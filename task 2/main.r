# Charger les données
data <- read.csv('dataset/Housing.csv')

# Histogramme pour la colonne 'bedrooms'
hist(data$bedrooms, 
     breaks=15, 
     col='blue', 
     main='Histogramme des chambres à coucher', 
     xlab='Nombre de chambres', 
     ylab='Fréquence')

# Graphique de dispersion pour 'area' et 'price'
plot(data$area, 
     data$price, 
     main='Graphique de dispersion: Surface - Prix',
     xlab='Surface (pieds carrés)', 
     ylab='Prix (USD)', 
     col='red', 
     pch=19)
