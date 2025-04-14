from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import os
from dotenv import load_dotenv
class LLaMAHelper:
    def __init__(self, hf_token=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_id = "meta-llama/Llama-3.2-3B-Instruct"
        load_dotenv()
        hf_token = hf_token or os.getenv("HF_TOKEN")

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, token=hf_token)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            token=hf_token,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        ).to(self.device)

        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if torch.cuda.is_available() else -1
        )

    #     self.text_classifier = pipeline("zero-shot-classification", model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli")
        
    # def classifier(self, text, candidate_labels):
    #     return self.text_classifier(text, candidate_labels)
    
    def chat(self, system_prompt, prompt, max_new_tokens=300, temperature=0.5):
        messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ]
        outputs = self.pipe(messages, max_new_tokens=max_new_tokens, do_sample=True, temperature=temperature)
        if outputs:
            if "content" in outputs[0]["generated_text"][-1]:
                full_response = outputs[0]["generated_text"][-1]["content"].lower()
            else:
                full_response = outputs[0]["generated_text"][-1].lower()

        print('response from LLM is', full_response)
        return full_response.replace(prompt, "").strip()

