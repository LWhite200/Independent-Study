# local_ai_working.py
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load names
with open("names.txt", "r", encoding="utf-8") as f:
    names = [line.strip() for line in f if line.strip()]

print("Names:", names)
print("Loading Phi-3...")

# Load model directly
tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True,
    attn_implementation="eager"  # Force eager to avoid flash-attention issues
)

print("✅ Phi-3 loaded!")

def compare_names(name1, name2):
    """Tool function for the AI to use"""
    if name1.lower() < name2.lower():
        return f"'{name1}' comes before '{name2}'"
    else:
        return f"'{name2}' comes before '{name1}'"

# Create a prompt that forces the AI to think through sorting
prompt = f"""You need to sort these names alphabetically: {', '.join(names)}

You have access to a comparison function that tells you which of two names comes first.

Think step by step:
1. Compare pairs of names using the comparison function
2. Figure out the correct alphabetical order
3. Return the final sorted list

After you determine the order, return ONLY: Sorted names: [comma separated list]

Let's start comparing:"""

print("\n🤖 Asking AI to sort names...")
print("Prompt:", prompt[:200] + "...")

# Tokenize and generate
inputs = tokenizer(prompt, return_tensors="pt", max_length=2048, truncation=True).to(model.device)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=500,
        do_sample=True,
        temperature=0.3,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id
    )

# Get response
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
ai_response = response[len(prompt):].strip()  # Get only the AI's part

print("\n🧠 AI Thinking:")
print(ai_response)

# Show correct answer
correct_sorted = sorted(names, key=lambda x: x.lower())
print(f"\n✅ CORRECT ORDER: {', '.join(correct_sorted)}")