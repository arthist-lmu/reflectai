import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

#mps
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("MPS available")
else:
    device = torch.device("cpu")

tokenizer = AutoTokenizer.from_pretrained("ibm/knowgl-large")
model = AutoModelForSeq2SeqLM.from_pretrained("ibm/knowgl-large").to(device)

input_text = "There are two kneeling angels, one holding Jesus's garment, and the other with its hands folded, both in front of the symbolization of salvation and life, the palm tree.[2] While barefoot in the river, John the Baptist is clothed in robes with a halo over his head."

inputs = tokenizer(input_text, return_tensors="pt").to(device)

num_beams = 5
output = model.generate(**inputs, max_length=1000, num_beams=num_beams)

decoded_output = tokenizer.decode(output[0].to('cpu'), skip_special_tokens=True)

print(decoded_output)