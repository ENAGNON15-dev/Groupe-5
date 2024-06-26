import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import time
from diffusers import StableDiffusionPipeline
import torch


# Charger le modèle
pipe = StableDiffusionPipeline.from_pretrained("hf-internal-testing/tiny-stable-diffusion-torch")  # Avec tiny-stable-diffusion-pipe

#device = "cuda" if torch.cuda.is_available() else "cpu"
#pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16).to(device)

# Dimensions d'une page PowerPoint standard
ppt_width = 980
ppt_height = 500

class ImageGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Generator App")
        self.root.geometry(f"{ppt_width}x{ppt_height}")
        self.root.resizable(False, False)  # Empêche le redimensionnement de la fenêtre

        self.setup_pages()

    def setup_pages(self):
        # Charger les images de fond
        self.background_path = "r.jpg"
        self.background_img = Image.open(self.background_path).resize((ppt_width, ppt_height), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_img)

        self.new_page_image_path = "b.jpg"
        self.new_page_img = Image.open(self.new_page_image_path).resize((ppt_width, ppt_height), Image.LANCZOS)
        self.new_page_photo = ImageTk.PhotoImage(self.new_page_img)

        # Créer les pages
        self.page1 = tk.Frame(self.root, width=ppt_width, height=ppt_height)
        self.canvas1 = tk.Canvas(self.page1, width=ppt_width, height=ppt_height)
        self.canvas1.pack(fill="both", expand=True)
        self.canvas1.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.page2 = tk.Frame(self.root, width=ppt_width, height=ppt_height)
        self.canvas2 = tk.Canvas(self.page2, width=ppt_width, height=ppt_height)
        self.canvas2.pack(fill="both", expand=True)
        self.canvas2.create_image(0, 0, image=self.new_page_photo, anchor="nw")

        self.create_page1_widgets()
        self.create_page2_widgets()

        self.page1.pack(fill="both", expand=True)

    def create_page1_widgets(self):
        button_width = 300
        button_height = 50
        button_x = ppt_width / 2 - button_width / 2 - 20
        button_y = ppt_height - 150 + 20
        button = self.round_rectangle(self.canvas1, button_x, button_y, button_x + button_width, button_y + button_height, radius=20, fill="#7C83FD", outline="")
        button_text = self.canvas1.create_text(button_x + button_width / 2, button_y + button_height / 2, text="Commencez par créer", fill="white", font=("Arial", 16, "bold"))
        arrow_size = 20
        arrow_x1 = button_x + button_width - arrow_size - 10
        arrow_y1 = button_y + button_height / 2 - arrow_size / 2
        arrow_x2 = button_x + button_width - 10
        arrow_y2 = button_y + button_height / 2 + arrow_size / 2
        arrow = self.canvas1.create_polygon(arrow_x1, arrow_y1, arrow_x2, button_y + button_height / 2, arrow_x1, arrow_y2, fill="white")

        self.canvas1.tag_bind(button, "<Button-1>", lambda event: self.show_new_page())
        self.canvas1.tag_bind(button_text, "<Button-1>", lambda event: self.show_new_page())
        self.canvas1.tag_bind(arrow, "<Button-1>", lambda event: self.show_new_page())

    def create_page2_widgets(self):
        self.text_box_width = 300
        self.text_box_height = 200
        description_zone_x = 35
        description_zone_y = 200
        description_zone_width = 400
        description_zone_height = 200

        text_box_x = description_zone_x + (description_zone_width - self.text_box_width) // 2
        text_box_y = description_zone_y + (description_zone_height - self.text_box_height) // 2

        self.text_box = tk.Text(self.page2, width=50, height=10, bg='#FFFFFF', fg='black', font=("Arial", 12), bd=0, highlightthickness=0)
        self.text_box.place(x=text_box_x, y=text_box_y, width=self.text_box_width, height=self.text_box_height)

        generate_button_x = ppt_width // 2 - 35
        generate_button_y = 300 - 35

        self.generate_button = tk.Button(self.page2, text="Générer", bg="#7C83FD", fg="white", font=("Arial", 12, "bold"), command=self.generate_image)
        self.generate_button.place(x=generate_button_x, y=generate_button_y, width=70, height=70)

        self.progress_label = ttk.Label(self.page2, text="Chargement en cours...")
        self.progress_bar = ttk.Progressbar(self.page2, orient='horizontal', mode='indeterminate', length=200)

        style = ttk.Style()
        style.theme_use('default')
        style.configure('TProgressbar', troughcolor='white', background='purple', thickness=10)

        self.image_canvas = tk.Canvas(self.page2, width=300, height=200, bg="white")
        self.image_canvas.place(x=ppt_width - 400, y=230)

        self.caption_label = ttk.Label(self.page2, text="", wraplength=200)
        self.caption_label.place(x=ppt_width - 300, y=-300)

    def round_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def show_new_page(self):
        self.page1.pack_forget()
        self.page2.pack(fill="both", expand=True)

    def generate_image(self):
        def run_generation():
            prompt = self.text_box.get("1.0", tk.END).strip()
            if not prompt:
                prompt = "a photo of an astronaut riding a horse on mars"

            # Simulate the time delay for generation
            for i in range(100):
                self.progress_bar['value'] = i + 1
                self.root.update_idletasks()
                time.sleep(0.05)

            # Here you should call your model to generate the image
            image = self.generate_image_with_model(prompt)

            # Display the generated image
            image.thumbnail((300, 200))
            photo = ImageTk.PhotoImage(image)
            self.image_canvas.create_image(0, 0, anchor="nw", image=photo)
            self.image_canvas.image = photo

            self.caption_label.config(text=prompt)

            # Hide the progress bar and enable the button
            self.progress_bar.pack_forget()
            self.progress_label.pack_forget()
            self.generate_button.config(state=tk.NORMAL)

        self.progress_label.place(x=ppt_width - 400, y=200)
        self.progress_bar.place(x=ppt_width - 400, y=220)
        self.progress_bar.start()
        self.generate_button.config(state=tk.DISABLED)

        thread = threading.Thread(target=run_generation)
        thread.start()

    def generate_image_with_model(self, prompt):
        description = self.text_box.get("1.0", "end-1c")
        self.progress_bar.pack(pady=20)
        self.progress_bar.start()

        try:
            print(f"Prompt: {description}")  # Debug: Afficher le prompt
            image = pipe(description).images[0]

            # Afficher les dimensions originales de l'image pour le débogage
            original_width, original_height = image.size
            print(f"Original image size: {original_width}x{original_height}")  # Debug: Afficher les dimensions originales

            # Redimensionner l'image proportionnellement
            new_size = (300, 200)
            image = image.resize(new_size, Image.ANTIALIAS)

            # Afficher les dimensions redimensionnées de l'image pour le débogage
            resized_width, resized_height = image.size
            print(f"Resized image size: {resized_width}x{resized_height}")  # Debug: Afficher les dimensions redimensionnées

            photo = ImageTk.PhotoImage(image)
            self.image_canvas.create_image(0, 0, anchor="nw", image=photo)
            self.image_canvas.image = photo
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "An error occurred while generating the image.")
        finally:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()  # Masquer la barre de progression après génération
            self.progress_label.pack_forget()
            self.generate_button.config(state=tk.NORMAL)

        return image

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageGeneratorApp(root)
    root.mainloop()
