import numpy as np
from PIL import Image


# 0 = Negro = pared
# 1 = Blanco = camino

def get_matrix(mapName):
    img = Image.open(mapName).convert("L")
    matriz = np.array(img)
    return matriz


def getColition(map1, position):
    x, y = position
    
    if map1[x][y] == 0:
        return True
    return False

def main():
    ...
if __name__ =="__main__":
    main()