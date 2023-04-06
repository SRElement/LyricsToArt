import argparse
import os
from PIL import Image
from min_dalle import MinDalle
import torch
class MinDalleTextToImage():
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--mega', action='store_true')
        self.parser.add_argument('--no-mega', dest='mega', action='store_false')
        self.parser.set_defaults(mega=False)
        self.parser.add_argument('--fp16', action='store_true')
        self.parser.add_argument('--text', type=str, default='sad face')
        self.parser.add_argument('--seed', type=int, default=-1)
        self.parser.add_argument('--grid-size', type=int, default=1)
        self.parser.add_argument('--image-path', type=str, default='generated')
        self.parser.add_argument('--models-root', type=str, default='pretrained')
        self.parser.add_argument('--top_k', type=int, default=256)
        self.parser.add_argument('--file-dir', type=str, default="generated_images")
        #self.args = self.parser.parse_args()
        self.args, self.unknown = self.parser.parse_known_args()

    def __args__(self):
        return self.args

    def save_image(self, image: Image.Image, path: str, fileDir: str):
        if os.path.isdir(path):
            path = os.path.join(path, '.png')
        elif not path.endswith('.png'):
            path += '.png'
        if not(os.path.exists(fileDir)):
            os.mkdir(fileDir)
        print("saving image to", path)
        image.save(fileDir + '/' + path)
        return image
    
    def generate_image(
        self,
        is_mega: bool,
        text: str,
        seed: int,
        grid_size: int,
        top_k: int,
        image_path: str,
        models_root: str,
        fp16: bool,
        file_dir: str
    ):
        model = MinDalle(
            is_mega=is_mega, 
            models_root=models_root,
            is_reusable=False,
            is_verbose=True,
            dtype=torch.float16 if fp16 else torch.float32
        )

        image = model.generate_image(
            text, 
            seed, 
            grid_size, 
            top_k=top_k, 
            is_verbose=True
        )
        self.save_image(image, image_path, file_dir)