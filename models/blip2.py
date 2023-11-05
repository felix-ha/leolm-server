import requests
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch

def run():
    processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
    model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16, device_map="auto")

    img_url = 'https://hips.hearstapps.com/clv.h-cdn.co/assets/16/18/gettyimages-569175741-1.jpg' 
    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

    question = "how many dogs are in the picture?"
    inputs = processor(raw_image, question, return_tensors="pt").to("cuda", torch.float16)

    out = model.generate(**inputs)

    return processor.decode(out[0], skip_special_tokens=True).strip()
