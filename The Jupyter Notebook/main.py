from transformers import MT5Tokenizer, MT5ForConditionalGeneration, Trainer, TrainingArguments
from datasets import load_dataset
import pandas as pd
import numpy as np
from datasets import load_dataset

model_name = "google/mt5-large"
tokenizer = MT5Tokenizer.from_pretrained("google/mt5-small")


def main() -> None:
    data = load_dataset("SKNahin/bengali-transliteration-data")
    df = data["train"].to_pandas()
    df.to_csv('amalgam.csv', index=False)

    dataset = load_dataset('csv', data_files={'train': 'amalgam.csv'})
    tokenized_datasets = dataset["train"].map(preprocess_function, batched=True)
    model = MT5ForConditionalGeneration.from_pretrained(model_name)

    training_args = TrainingArguments(
        output_dir="./results",
        eval_strategy="no",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        save_total_limit=2,
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets,
    )

    trainer.train()

    trainer.save_model("trained_banglish_to_bangla_model")
    model = MT5ForConditionalGeneration.from_pretrained("trained_banglish_to_bangla_model")
    tokenizer = MT5Tokenizer.from_pretrained("trained_banglish_to_bangla_model")

    run_state_machine() 


def run_state_machine() -> None:
    while True:
        user_input = input("Enter Banglish text: ")
        if user_input.lower() == "exit":
            break
        translated_output = translate_banglish_to_bangla(user_input)
        print("Bangla translation:", translated_output)


def preprocess_function(examples: dict[str, str]) -> dict[str, str]:
    inputs = examples["rm"]
    targets = examples["bn"]
    model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")
    labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length")
    model_inputs["labels"] = labels["input_ids"]
    
    return model_inputs


def translate_banglish_to_bangla(banglish_text: str) -> str:
    inputs = tokenizer(banglish_text, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**inputs)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return translated_text


if __name__ == "__main__":
    main()
