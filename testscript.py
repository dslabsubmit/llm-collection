#测试类推理是否正确
from deepseekcoder_v2lite import deepseekcoder_v2lite

def test_model():
    model = deepseekcoder_v2lite()
    input_text = "Write a simple Python function to calculate the sum of two numbers."
    output = model.run_model(input_text)
    print("生成的代码:\n", output)

if __name__ == "__main__":
    test_model()