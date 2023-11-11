import requests
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch


def run():
    processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
    model = Blip2ForConditionalGeneration.from_pretrained(
        "Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16, device_map="auto"
    )

    img_url = "https://hips.hearstapps.com/clv.h-cdn.co/assets/16/18/gettyimages-569175741-1.jpg"
    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert("RGB")

    question = "how many dogs are in the picture?"
    qtext = f"Question: {question} Answer:"
    inputs = processor(raw_image, qtext, return_tensors="pt").to("cuda", torch.float16)

    decoding_method = "Nucleus sampling"

    out = model.generate(
        **inputs,
        do_sample=decoding_method == "Nucleus sampling",
        temperature=1.0,
        length_penalty=1.0,
        repetition_penalty=1.5,
        max_length=50,
        min_length=1,
        num_beams=5,
        top_p=0.9,
    )

    return processor.decode(out[0], skip_special_tokens=True).strip()
