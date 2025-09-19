# local_runner.py

from agents import Runner
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class LocalRunner(Runner):
    # Larger, instruction-tuned model
    MODEL_NAME = "google/flan-t5-large"

    # Load once to speed up repeated calls
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

    @staticmethod
    def run_sync(agent, prompt, max_tokens=150, exact_word_count=None):
        """
        Run the local instruction-tuned LLM with optional exact word count enforcement.
        """
        # Prompt engineering for strict instruction following
        engineered_prompt = (
            f"You are a helpful assistant. Follow instructions exactly.\n"
            f"Instruction: {prompt}"
        )

        inputs = LocalRunner.tokenizer(engineered_prompt, return_tensors="pt")

        # Beam search for better structured output
        outputs = LocalRunner.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            num_beams=5,
            early_stopping=True
        )

        text = LocalRunner.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Optional: enforce exact word count
        if exact_word_count is not None:
            words = text.split()
            if len(words) > exact_word_count:
                words = words[:exact_word_count]
            elif len(words) < exact_word_count and words:
                words += [words[-1]] * (exact_word_count - len(words))
            text = " ".join(words)

        # Wrap in Result object
        class Result:
            def __init__(self, output):
                self.final_output = output

        return Result(text)
