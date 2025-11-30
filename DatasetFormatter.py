import os
import random
import shutil

random.seed(1)

#Este scipt crea el directorio validation en el dataset original, lo rellena y crea un subconjunto
#de 10 clases del dataset.


#Este script se ejecuta sobre el directorio original del dataset (el que contiene las carpetas train y test)
#Por tanto, solo mostrará una funcionalidad aparente si no existen las validation, sus subcarpertas, o si estas
#están vacías. Se puede observar su ejecución borrando cualquiera de las mencionadas anteriormente, pero no se
#recomienda ya que se modificarán las proporciones del dataset fuera de las esperadas (10-80-10 para test-train-val)
#Para su prueba se recomienda aplicarse sobre el conjunto de datos original, renombrado a SkinDisease(22 clases).

project_dir = os.path.join(os.getcwd()) #Puede ser inconsistente dependiendo del IDE

val_dir = os.path.join(project_dir, "SkinDisease(22 clases)", "validation")
train_dir = os.path.join(project_dir, "SkinDisease(22 clases)", "train")


if not os.path.exists(val_dir):
    os.mkdir(val_dir)

for dir in os.listdir(train_dir):
    if not os.path.exists(os.path.join(val_dir, dir)):
        os.mkdir(os.path.join(val_dir, dir))
    target = os.path.join(val_dir, dir)
    source = os.path.join(train_dir, dir)
    if len(os.listdir(target)) != 0:
           continue
    for file in os.listdir(source):
        if random.randint(1, 9) == 9:
            os.rename(os.path.join(source, file), os.path.join(target, file))


subset_dir=os.path.join(project_dir, "SkinDisease(10 clases)")

if not os.path.exists(subset_dir):
    os.mkdir(subset_dir)

if len(subset_dir) != 0:
    exit

chosen = []

while len(chosen)<10:
    x=random.randint(0, 21)
    if x in chosen:
        continue
    chosen.append(x)

for num in chosen:
    disease=os.listdir(train_dir)[num]
    shutil.copytree(os.path.join(train_dir, disease), os.path.join(subset_dir, "train", disease))
    shutil.copytree(os.path.join(val_dir, disease), os.path.join(subset_dir, "validation", disease))
    shutil.copytree(os.path.join(project_dir, "SkinDisease(22 clases)", "test", disease), os.path.join(subset_dir, "test", disease))

print("Done")