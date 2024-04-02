# srun --pty -w devbox5 -c 6 --mem 24G --gres=gpu:1 zsh 
import requests
from PIL import Image

url = 'https://previous.bildindex.de/bilder/fmd10024339a.jpg' 
image = Image.open(requests.get(url, stream=True).raw).convert('RGB')  
from transformers import AutoProcessor, Blip2ForConditionalGeneration
import torch

processor = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
# by default `from_pretrained` loads the weights in float32
# we load in float16 instead to save memory
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16) 
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
prompt = "the color scheme of this painting is composed of"
print("Prompt: " + prompt)

inputs = processor(image, text=prompt, return_tensors="pt").to(device, torch.float16)

generated_ids = model.generate(**inputs, max_new_tokens=20)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
print(generated_text)