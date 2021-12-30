import os
import shutil

annotations_folder = "annotations"
train_images = os.listdir('train/images')
val_images = os.listdir('val/images')

for img in train_images:
    name = os.path.splitext(img)[0]
    annotation = os.path.join(annotations_folder, name + '.xml')
    try:
        shutil.copy(annotation, "train/labels/" + name + ".xml")
    except IOError as e:
        print(f"Can't copy file {e}")

for img in val_images:
    name = os.path.splitext(img)[0]
    annotation = os.path.join(annotations_folder, name + '.xml')
    try:
        shutil.copy(annotation, "val/labels/" + name + ".xml")
    except IOError as e:
        print(f"Can't copy file {e}")