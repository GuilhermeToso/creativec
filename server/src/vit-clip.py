import os
from tqdm import tqdm
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer, BlipProcessor, BlipForConditionalGeneration
import torch
from PIL import Image
import csv

def useViT(filenames):

    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    #
    # gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

    results = []

    for i in tqdm(range(len(filenames))):
        image_path = filenames[i]
        image = Image.open(image_path)
        if image.mode != "RGB":
            image = image.convert(mode="RGB")

        pixel_values = feature_extractor(images=[image], return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)

        output_ids = model.generate(pixel_values, **gen_kwargs)

        preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        value = [image_path, [pred.strip() for pred in preds][0]]
        results.append(value)
        print(value)
    
    with open("vit.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(results)

    return results

def useBlip(filenames):

    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("cuda")

    results = []
    for i in tqdm(range(len(filenames))):
        image_path = filenames[i]
        image = Image.open(image_path)
        if image.mode != "RGB":
            image = image.convert(mode="RGB")

        inputs = processor(image, return_tensors="pt").to("cuda")
        out = model.generate(**inputs)
        text = processor.decode(out[0], skip_special_tokens=True)
        results.append([image_path, text])
    with open("blip.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(results)

    return results

class Image2Text():
  
    def __init__(self, model:str = "blip") -> None:

        
        self.path = os.path.join(os.getcwd(),"server/assets")
        self.model = model


    def get_filenames(self):
        """
        List all files in the raw directory.

        Returns:
        - list: A list of filenames in the raw directory.

        Raises:
        - ValueError: If the raw directory path is invalid.
        """
        path = self.path + "/preprocessed"
        if not os.path.isdir(path):
            raise ValueError(f"'{path}' is not a valid directory.")
        
        files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        
        return files


    def predict(self):

        filenames = self.get_filenames()
        if self.model =="blip":
            return useBlip(filenames)
        elif self.model == "vit":
            return useViT(filenames)
        

i2s = Image2Text("blip")
i2s.predict()