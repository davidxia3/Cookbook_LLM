# Cookbook LLM: Fine Tuning GPT-2 for Recipe-Based Text Generation

This project is focused on fine tuning a GPT-2 model to generate text completions for recipe-related prompts. The model is trained to answer questions such as "What ingredients are in {recipe}?" and "What aisle is {ingredient} in?" using a custom dataset of recipes and ingredients. The goal of the project is to make it easier for users to know what ingredients are in recipes and where to find them in a store more efficiently.

## Setup

1. Clone the repository:
```bash
   git clone https://github.com/davidxia3/Cookbook-LLM.git
   cd Cookbook-LLM
```

2. Install dependencies:
```bash
    pip install -r requirements.txt
```

3. Train custom model
```bash
python src/training.py
```

## Usage
After training, you can use the fine-tuned model to generate text completions for recipe-related questions:
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("./models")
model = AutoModelForCausalLM.from_pretrained("./models")

prompt = "What ingredients are in chocolate chip cookies?"
input_ids = tokenizer(prompt, return_tensors="pt").input_ids

output = model.generate(input_ids)
print(tokenizer.decode(output[0], skip_special_tokens=True))
```


