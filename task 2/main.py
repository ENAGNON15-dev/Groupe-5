import pandas as pd
import matplotlib.pyplot as plt

# Charger les données
data = pd.read_csv('dataset/Housing.csv')


while True:
    print("\n1. Histogramme \n2. Graphique de dispersion\n\t")
    choice = input("Votre choix : ")

    if choice == '1':
        # Histogramme pour la colonne 'bedrooms'

        plt.figure(figsize=(10, 6))
        plt.hist(data['bedrooms'], bins=15, color='blue', edgecolor='black')
        plt.title('Histogramme des chambres à coucher')
        plt.xlabel('Nombre de chambres')
        plt.ylabel('Fréquence')
        plt.grid(True)
        plt.show()

        break
    elif choice == '2':
        # Graphique de dispersion pour 'area' et 'price'

        plt.figure(figsize=(10, 6))
        plt.scatter(data['area'], data['price'], color='red', edgecolor='black')
        plt.title('Graphique de dispersion: Surface - Prix')
        plt.xlabel('Surface (pieds carrés)')
        plt.ylabel('Prix (USD)')
        plt.grid(True)
        plt.show()

        break
    else:
        continue
