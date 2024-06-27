class Array:
    def __init__(self, data):
        if isinstance(data[0], list):  
            # pour 2D
            self.data = data
            self.shape = (len(data), len(data[0]))
            # pour 1D
        else:  
            self.data = data
            self.shape = (len(data),)

    def __len__(self):
        return self.shape[0]

    def __add__(self, other): # pour l'adition
        if isinstance(other, Array):
            if self.shape != other.shape:
                raise ValueError("Les formes  ne sont pas pareilles.")
            if len(self.shape) == 1:
                return Array([self.data[i] + other.data[i] for i in range(len(self.data))])
            else:
                return Array([[self.data[i][j] + other.data[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])])
        else:  
            if len(self.shape) == 1:
                return Array([x + other for x in self.data])
            else:
                return Array([[x + other for x in row] for row in self.data])

        def __sub__(self, other): # pour la soustraction
        if isinstance(other, Array):
            if self.shape != other.shape:
                raise ValueError("Les formes  ne sont pas pareilles")
            if len(self.shape) == 1:
                return Array([self.data[i] - other.data[i] for i in range(len(self.data))])
            else:
                return Array([[self.data[i][j] - other.data[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])])
        else:  
            if len(self.shape) == 1:
                return Array([x - other for x in self.data])
            else:
                return Array([[x - other for x in row] for row in self.data])

    def __mul__(self, other): # pour la multiplication
        if isinstance(other, Array):
            if self.shape != other.shape:
                raise ValueError("Les formes  ne sont pas pareilles.")
            if len(self.shape) == 1:
                return Array([self.data[i] * other.data[i] for i in range(len(self.data))])
            else:
                return Array([[self.data[i][j] * other.data[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])])
        else:  
            if len(self.shape) == 1:
                return Array([x * other for x in self.data])
            else:
                return Array([[x * other for x in row] for row in self.data])

    def __truediv__(self, other): # pour la division
        if isinstance(other, Array):
            if self.shape != other.shape:
                raise ValueError("Les formes  ne sont pas pareilles.")
            if len(self.shape) == 1:
                return Array([self.data[i] / other.data[i] for i in range(len(self.data))])
            else:
                return Array([[self.data[i][j] / other.data[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])])
        else:  
            if len(self.shape) == 1:
                return Array([x / other for x in self.data])
            else:
                return Array([[x / other for x in row] for row in self.data])

    def __matmul__(self, other):  # pour le produit scalaire
        if self.shape != other.shape or len(self.shape) != 1:
            raise ValueError("Uniquement pour les array de 1D et de même longueur.")
        return sum(self.data[i] * other.data[i] for i in range(len(self.data)))

    def __contains__(self, item): # pour l'opérateur in
        if len(self.shape) == 1:
            return item in self.data
        else:
            return any(item in row for row in self.data)

    def __getitem__(self, index):
        if isinstance(index, tuple):
            if isinstance(index[0], slice) or isinstance(index[1], slice):
                return Array([row[index[1]] for row in self.data[index[0]]])
            else:
                return self.data[index[0]][index[1]]
        elif isinstance(index, slice):
            return Array(self.data[index])
        else:
            return self.data[index]

    def __repr__(self):
        return f"Array({self.data})"


# Exemple d'utilisation
a = Array([1, 2, 3])
b = Array([4, 5, 6])
print(a + b)            # Array([5, 7, 9])
print(a - b)            # Array([-3, -3, -3])
print(a * b)            # Array([4, 10, 18])
print(a / b)            # Array([0.25, 0.4, 0.5])
print(a @ b)            # 32
print(2 in a)           # True
print(a[1])             # 2
print(a[1:3])           # Array([2, 3])

c = Array([[1, 2], [3, 4]])
d = Array([[5, 6], [7, 8]])
print(c + d)            # Array([[6, 8], [10, 12]])
print(c[1, 1])          # 4
print(c[0:2, 0])        # Array([1, 3])