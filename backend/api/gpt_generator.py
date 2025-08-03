# backend/services/gpt_generator.py

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging

logger = logging.getLogger(__name__)


class GPT2Generator:
    def __init__(self, model_name="distilgpt2"):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            # Set pad_token to eos_token to resolve padding errors
            self.tokenizer.pad_token = self.tokenizer.eos_token

            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            logger.info(f"Loaded GPT model: {model_name}")
        except Exception as e:
            logger.error("Failed to load GPT model", exc_info=True)
            raise RuntimeError("Could not load GPT2 model")

    def generate_summary(self, context: str, max_new_tokens: int = 100) -> str:
        if not context.strip():
            return "No relevant documents found to generate a response."

        try:
            prompt = f"Based on the following information, give a meaningful response:\n{context}\nAnswer:"
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            )
            input_ids = inputs["input_ids"]
            attention_mask = inputs["attention_mask"]

            output = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=max_new_tokens,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                early_stopping=True,
                pad_token_id=self.tokenizer.pad_token_id,
            )

            return self.tokenizer.decode(output[0], skip_special_tokens=True)
        except Exception as e:
            logger.error("GPT2 generation failed", exc_info=True)
            return "An error occurred while generating the response."
