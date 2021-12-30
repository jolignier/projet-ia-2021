import xml.etree.ElementTree as ET
import yaml

from tqdm import tqdm
from utils.general import download, Path



def convert_label(path, lb_path, image_id):
  def convert_box(size, box):
      dw, dh = 1. / size[0], 1. / size[1]
      x, y, w, h = (box[0] + box[1]) / 2.0 - 1, (box[2] + box[3]) / 2.0 - 1, box[1] - box[0], box[3] - box[2]
      return x * dw, y * dh, w * dw, h * dh

  in_file = open(path / f'voc_labels/{image_id}.xml')
  print(in_file)
  out_file = open(lb_path, 'w')
  tree = ET.parse(in_file)
  root = tree.getroot()
  size = root.find('size')
  w = int(size.find('width').text)
  h = int(size.find('height').text)

  for obj in root.iter('object'):
      cls = obj.find('name').text
      if cls in yaml['names'] and not int(obj.find('difficult').text) == 1:
          xmlbox = obj.find('bndbox')
          bb = convert_box((w, h), [float(xmlbox.find(x).text) for x in ('xmin', 'xmax', 'ymin', 'ymax')])
          cls_id = yaml['names'].index(cls)  # class id
          out_file.write(" ".join([str(a) for a in (cls_id, *bb)]) + '\n')


# Download
dir = Path(yaml['path'])  # dataset root dir
for image_set in ('train', 'val'):
  path = dir / f'{image_set}/'
  imgs_path = path / f'images/'
  old_lbs_path = path / f'voc_labels/'
  new_lbs_path = path / f'yolo_labels/'

  image_ids = open(path / f'images.txt').read().strip().split()
  for id in tqdm(image_ids, desc=f'{image_set}'):
      f = imgs_path / f'{id}.jpg'  # img path
      lb_path = (new_lbs_path / f.name).with_suffix('.txt')  # new label path

      convert_label(path, lb_path, id)  # convert labels to YOLO format
