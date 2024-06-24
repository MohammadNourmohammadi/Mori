from encoder.abstract import Encoder
import torch
import numpy as np
from PIL import Image
import PIL
import clip
import requests
from io import BytesIO
import os

class ClipModel(Encoder):

    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # model_path = os.environ.get("VIT_B32_PATH", "/Users/mohammad/Desktop/mori/backend/data/model/vit_b32.pth")
        # state_dict = torch.load(model_path, map_location=self.device)
        # model.load_state_dict(state_dict)
        model, preprocess = clip.load("ViT-B/32", device=self.device)
        self.model = model
        self.preprocess = preprocess
    
    
    def encode_text(self, text: str):
        text_input = clip.tokenize([text]).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text_input)
        return np.array(text_features[0])
    
    def encode_image(self, images: str):
        response = requests.get(images)
        image = PIL.Image.open(BytesIO(response.content))
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
        return np.array(image_features[0])
    
