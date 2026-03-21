from llm import *


class DeepSeek_R1_70B(LLM):
    def __init__(self):
        self.load_model()

    def load_model(self):
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch

        # Load the model with multi-GPU support and mixed precision
        self.model = AutoModelForCausalLM.from_pretrained(
            "/home/yhr/data/modelscope/hub/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/",
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,  # Use BFloat16 for better performance and memory efficiency
            low_cpu_mem_usage=True,  # Efficiently load large models by reducing CPU memory usage
            device_map="auto",  # Automatically distribute the model across available GPUs
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            "/home/yhr/data/modelscope/hub/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/",
            model_max_length=self.model.config.max_position_embeddings
        )

    @cost_time
    def run_model(self, input_text):
        chat = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": input_text},
        ]
        inputs = self.tokenizer.apply_chat_template(chat, return_tensors="pt")
        inputs = inputs.to("cuda")  # Move inputs to GPU

        # Generate the output
        output = self.model.generate(
            input_ids=inputs,
            max_new_tokens=self.max_new_tokens,
            max_length=self.max_length,
            max_time=self.max_time,
        )

        # Move the output to CPU and decode
        output = output[0].to("cpu")
        return self.tokenizer.decode(output, skip_special_tokens=True)