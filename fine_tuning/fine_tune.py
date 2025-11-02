import json
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments

# Step 1: Load Config
with open("fine_tuning/config.json") as f:
    config = json.load(f)

# Step 2: Load Dataset
with open("fine_tuning/dataset.json") as f:
    data = json.load(f)

inputs = [item["input"] for item in data]
outputs = [item["output"] for item in data]

# Step 3: Load Model & Tokenizer
model_name = config["model_name"]
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Step 4: Prepare Dataset
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

# Step 5: Training Config
args = TrainingArguments(
    output_dir=config["save_dir"],
    per_device_train_batch_size=config["batch_size"],
    num_train_epochs=config["epochs"],
    learning_rate=config["learning_rate"],
    save_total_limit=1
)

# Step 6: Trainer Setup
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset
)

# Step 7: Train & Save
trainer.train()
model.save_pretrained(config["save_dir"])
tokenizer.save_pretrained(config["save_dir"])

print("✅ Fine-tuning completed! Model saved at:", config["save_dir"])

