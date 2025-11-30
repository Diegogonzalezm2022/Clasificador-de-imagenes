import os
from PIL import Image

#Se espera que este script se aplica en el mismo directorio que SkinDisease(22 clases), existiendo este.

max_height=0
max_width=0
modes=[]
for dir in os.listdir(os.path.join(".", "SkinDisease(22 clases)")):
    for category in os.listdir(os.path.join(".", "SkinDisease(22 clases)", dir)):
        for image in os.listdir(os.path.join(".", "SkinDisease(22 clases)", dir, category)):
            current=Image.open(os.path.join(".", "SkinDisease(22 clases)", dir, category, image))
            if current.size[1]>max_height:
                max_height=current.size[1]
            if current.size[0]>max_width:
                max_width=current.size[0]
            if current.mode not in modes:
                modes.append(current.mode)

            
print(max_height, max_width, modes)