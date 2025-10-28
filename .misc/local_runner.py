# local_runner.py
from agents import Runner
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class LocalRunner(Runner):
    # Phi-3 Mini model
    MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
    
    _tokenizer = None
    _model = None
    
    @classmethod
    def _ensure_loaded(cls):
        if cls._tokenizer is None:
            print("Loading Phi-3 tokenizer...")
            cls._tokenizer = AutoTokenizer.from_pretrained(
                cls.MODEL_NAME, 
                trust_remote_code=True
            )
            
            print("Loading Phi-3 model...")
            cls._model = AutoModelForCausalLM.from_pretrained(
                cls.MODEL_NAME,
                dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
                attn_implementation="eager"  # Fix for flash-attention issue
            )
            print("✅ Phi-3 model loaded successfully!")

    @staticmethod
    def run_sync(agent, prompt, max_tokens=500):
        # Make sure model is loaded
        LocalRunner._ensure_loaded()
        
        # Phi-3 uses specific chat format
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        # Apply Phi-3's chat template
        formatted_prompt = LocalRunner._tokenizer.apply_chat_template(
            messages, 
            tokenize=False,
            add_generation_prompt=True
        )
        
        # Tokenize
        inputs = LocalRunner._tokenizer(
            formatted_prompt, 
            return_tensors="pt",
            return_attention_mask=True
        )
        
        # Move to device and ensure all required tensors are present
        input_ids = inputs['input_ids'].to(LocalRunner._model.device)
        attention_mask = inputs['attention_mask'].to(LocalRunner._model.device)
        
        # Generate response with compatibility fixes
        with torch.no_grad():
            outputs = LocalRunner._model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=max_tokens,
                do_sample=True,
                temperature=0.1,
                eos_token_id=LocalRunner._tokenizer.eos_token_id,
                pad_token_id=LocalRunner._tokenizer.eos_token_id,
                use_cache=False  # Disable cache to avoid the DynamicCache issue
            )
        
        # Extract only the assistant's response (skip the input prompt)
        response_ids = outputs[0][input_ids.shape[1]:]
        text = LocalRunner._tokenizer.decode(response_ids, skip_special_tokens=True).strip()
        
        # Wrap in Result object
        class Result:
            def __init__(self, output):
                self.final_output = output
        
        return Result(text)