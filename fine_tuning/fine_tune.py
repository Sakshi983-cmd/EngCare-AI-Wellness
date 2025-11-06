
from peft import get_peft_model, LoraConfig, TaskType
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import json

# Load config and dataset
with open("fine_tuning/config.json") as f:
    config = json.load(f)
with open("fine_tuning/dataset.json") as f:
    data = json.load(f)

inputs = [item["input"] for item in data]
outputs = [item["output"] for item in data]

# Tokenizer and base model
tokenizer = AutoTokenizer.from_pretrained(config["model_name"])
base_model = AutoModelForCausalLM.from_pretrained(config["model_name"])

# Apply LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["c_attn"],  # GPT2-specific; adjust for other models
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
model = get_peft_model(base_model, lora_config)

# Tokenize
input_encodings = tokenizer(inputs, truncation=True, padding=True)
output_encodings = tokenizer(outputs, truncation=True, padding=True)

class SimpleDataset:
    def __init__(self, encodings_in, encodings_out):
        self.encodings_in = encodings_in
        self.encodings_out = encodings_out

    def __getitem__(self, idx):
        return {
            "input_ids": self.encodings_in["input_ids"][idx],
            "labels": self.encodings_out["input_ids"][idx]
        }

    def __len__(self):
        return len(self.encodings_in["input_ids"])

train_dataset = SimpleDataset(input_encodings, output_encodings)

# Training
args = TrainingArguments(
    output_dir=config["save_dir"],
    per_device_train_batch_size=config["batch_size"],
    num_train_epochs=config["epochs"],
    learning_rate=config["learning_rate"],
    save_total_limit=1
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    tokenizer=tokenizer
)

trainer.train()
model.save_pretrained(config["save_dir"])
tokenizer.save_pretrained(config["save_dir"])
