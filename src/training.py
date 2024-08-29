import torch
from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments

dataset = load_dataset('json', data_files='data/jsonl_data/prompts.jsonl')

tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

def tokenize_function(examples):
    inputs = tokenizer(examples["prompt"], padding="max_length", truncation=True, max_length=512)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(examples["completion"], padding="max_length", truncation=True, max_length=512)
    
    inputs["labels"] = labels["input_ids"]
    return inputs

tokenized_dataset = dataset.map(tokenize_function, batched=True)

train_test_split = tokenized_dataset["train"].train_test_split(test_size=0.2)
tokenized_dataset = DatasetDict({
    'train': train_test_split['train'],
    'test': train_test_split['test']
})

model = AutoModelForCausalLM.from_pretrained("gpt2")

device = torch.device("mps" if torch.has_mps else "cpu")
model.to(device)


training_args = TrainingArguments(
    output_dir = "./training_output",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=2,
    num_train_epochs=5,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
)

trainer.train()

model.save_pretrained("./models")
tokenizer.save_pretrained("./models")
