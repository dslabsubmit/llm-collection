from llm import *
import torch
from modelscope import AutoTokenizer, Model, AutoModelForCausalLM
from accelerate import Accelerator

class deepseekcoder_v2lite(LLM):
    def __init__(self):
        self.load_model()

    def load_model(self):
        self.accelerator = Accelerator()

        self.model = AutoModelForCausalLM.from_pretrained(
            "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct/",
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
            #device_map="auto"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct/",
            trust_remote_code = True
        )
        # 准备模型
        self.model = self.accelerator.prepare(self.model)
        # 设置模型为评估模式
        self.model.eval()


    @cost_time
    def run_model(self, input_text):
        inputs = self.tokenizer(input_text, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs,
            max_new_tokens=self.max_new_tokens,
            max_length=self.max_length,
            max_time=self.max_time,
            #do_sample=True,
            #temperature=0.7,
            #top_p=0.9,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
