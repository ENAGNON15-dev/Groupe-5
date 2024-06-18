import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
from diffusers import StableDiffusionPipeline
import torch

# Charger le modèle
pipe = StableDiffusionPipeline.from_pretrained("hf-internal-testing/tiny-stable-diffusion-torch")  #Avec tiny-stable-diffusion-pipe

#device = "cuda" if torch.cuda.is_available() else "cpu"
#pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16).to(device)


# Fonction pour générer une image à partir d'une description
def generate_image(description, label_image, spinner):
    try:
        spinner.start()
        prompt = description.get()
        print(f"Prompt: {prompt}")  # Debug: Afficher le prompt
        image = pipe(prompt).images[0]

        # Afficher les dimensions originales de l'image pour le débogage
        original_width, original_height = image.size
        print(f"Original image size: {original_width}x{original_height}")  # Debug: Afficher les dimensions originales

        # Redimensionner l'image proportionnellement
        ratio = min(800 / original_width, 600 / original_height)
        new_size = (int(original_width * ratio), int(original_height * ratio))
        image = image.resize(new_size, Image.ANTIALIAS)

        # Afficher les dimensions redimensionnées de l'image pour le débogage
        resized_width, resized_height = image.size
        print(f"Resized image size: {resized_width}x{resized_height}")  # Debug: Afficher les dimensions redimensionnées

        # Convertir l'image en format compatible avec Tkinter
        tk_image = ImageTk.PhotoImage(image)

        # Mettre à jour l'étiquette pour afficher l'image générée
        label_image.config(image=tk_image)
        label_image.image = tk_image
        label_image.text = ''  # Clear any previous text

    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la génération de l'image : {e}")
    finally:
        spinner.stop()


# Fonction pour lancer le fil de génération d'image
def on_generate_button_click(description, label_image, spinner):
    threading.Thread(target=generate_image, args=(description, label_image, spinner)).start()


# Créer la fenêtre principale
root = tk.Tk()
root.title("Application de Génération d'Images")
root.geometry("900x700")  # Augmenter la taille de la fenêtre principale

# Créer et disposer les widgets
tk.Label(root, text="Description:").grid(row=0, column=0, padx=10, pady=10)

description = tk.Entry(root, width=50)
description.grid(row=0, column=1, padx=10, pady=10)

button_generate = tk.Button(root, text="Générer l'image",
                            command=lambda: on_generate_button_click(description, label_image, spinner))
button_generate.grid(row=1, column=1, pady=10)

spinner = ttk.Progressbar(root, mode='indeterminate')
spinner.grid(row=1, column=2, padx=10, pady=10)

label_image = tk.Label(root, text="Zone d'affichage de l'image", width=100, height=30)
label_image.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

# Permettre au label_image de s'étendre pour remplir l'espace disponible
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Lancer la boucle principale de Tkinter
root.mainloop()
