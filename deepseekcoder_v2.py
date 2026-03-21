from llm import *


class deepseekcoder_v2(LLM):
    def __init__(self):
        self.load_model()

    def load_model(self):
        import torch
        from modelscope import AutoTokenizer, Model

        self.model = Model.from_pretrained(
            "/home/yhr/data/modelscope/hub/deepseek-ai/DeepSeek-Coder-V2-Instruct/",
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            "/home/yhr/data/modelscope/hub/deepseek-ai/DeepSeek-Coder-V2-Instruct/"
        )

    @cost_time
    def run_model(self, input_text):
        inputs = self.tokenizer(input_text, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs,
            max_new_tokens=self.max_new_tokens,
            max_length=self.max_length,
            max_time=self.max_time,)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)