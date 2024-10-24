import os
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
from tqdm import tqdm
from .chroma import Chroma

class MultiModal:

    def __init__(self) -> None:
        self.model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
        self.path = self.get_project_root('creativec')
        self.data_path = os.path.join(self.path, "server", "assets", "data")
        self.chroma = Chroma()
        print(self.data_path)

    def get_project_root(self, root_folder_name: str):
        # Start at the current working directory
        current_path = os.getcwd()

        # Loop until the root of the file system is reached
        while current_path != os.path.dirname(current_path):
            # Check if the folder name 'creativec' is part of the path
            if os.path.basename(current_path) == root_folder_name:
                return current_path
            # Go up one directory
            current_path = os.path.dirname(current_path)

        raise FileNotFoundError(f"Project root '{root_folder_name}' not found.")

    def list_files(self):
        # Check if the directory exists
        if not os.path.exists(self.data_path):
            print(f"Directory {self.data_path} does not exist!")
            return []

        # List all files in the directory
        filenames = [f for f in os.listdir(self.data_path) if os.path.isfile(os.path.join(self.data_path, f))]

        # Sort filenames based on their integer values
        filenames.sort(key=lambda x: int(x.split('.')[0]))

        return filenames
    
    def get_texts(self, filename):
        # Initialize an empty list to store the extracted phrases
        phrases = []
        
        # Open the file in read mode
        with open(filename, 'r') as file:
            # Read all lines from the file
            lines = file.readlines()
        phrases = [line.split('. ', 1)[-1].strip('"\n') for line in lines if '. ' in line]
        
        return phrases

    def fewshot(self, image: str, text: list[str], similarity: str = "scaled"):

        img = Image.open(image)
        if img.mode != "RGB":
            img = img.convert(mode="RGB")

        inputs = self.processor(text=text, images=img, return_tensors="pt", padding=True)
        outputs = self.model(**inputs)
        image_embed = outputs.image_embeds
        text_embed = outputs.text_embeds

        if similarity == "scaled":

            similarities =  outputs.logits_per_image
            max_index = torch.argmax(similarities[0])
            maximum = similarities[0][max_index]
            chosen_text = text[max_index]
            
            output = {
                "image": image,
                "text":text,
                "image_embed": outputs.image_embeds.tolist()[0],
                "best_text": chosen_text,
                "best_text_embed": text_embed[max_index].tolist(),
            }
            return output
        elif similarity == "cos":

            similarities = torch.nn.functional.cosine_similarity(image_embed, text_embed)
            max_index = torch.argmax(similarities[0])
            maximum = similarities[max_index]
            chosen_text = text[max_index]
            
            output = {
                "image": image,
                "text":text,
                "image_embed": outputs.image_embeds.tolist()[0],
                "best_text": chosen_text,
                "best_text_embed": text_embed[max_index].tolist(),
            }
            return output
        elif similarity == "euclid":
            
            similarities = torch.cdist(image_embed, text_embed,p=2)
            max_index = torch.argmin(similarities[0])
            maximum = similarities[0][max_index]
            chosen_text = text[max_index]
            
            output = {
                "image": image,
                "text":text,
                "image_embed": outputs.image_embeds.tolist()[0],
                "best_text": chosen_text,
                "best_text_embed": text_embed[max_index].tolist(),
            }
            return output

    def run(self):
        
        files = self.list_files()

        
        for i in tqdm(range(len(files))):

            data = {"img-text":{"image":None,"text":None},"text":None}

            
            filename = os.path.join(self.data_path, files[i])
            texts = self.get_texts(filename)
            image = os.path.join(self.path, "server", "assets", "preprocessed", f"{i}.jpg")
            output = self.fewshot(image, texts)


            data["img-text"]["image"] = {
                "embedding":output["image_embed"],
                "document":output["best_text"],
                "id":str(i)
            }

            data["img-text"]["text"] = {
                "embedding": output["best_text_embed"],
                "document": output["best_text"],
                "id":str(i)
            }

            self.chroma.add_embed(data)

