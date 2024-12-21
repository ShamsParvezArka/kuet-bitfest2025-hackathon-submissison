from transformers import MT5Tokenizer, MT5ForConditionalGeneration, Trainer, TrainingArguments
from datasets import load_dataset
import pandas as pd
import numpy as np
from datasets import load_dataset


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