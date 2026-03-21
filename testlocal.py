# 测试本地模型是否正确
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained("/home/yhr/data/modelscope/hub/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("/home/yhr/data/modelscope/hub/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/", trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()

input_text = "#write a quick sort algorithm"
inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_length=256)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))