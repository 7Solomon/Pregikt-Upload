import os

import torch
import transformers

from transformers import LlamaForCausalLM, LlamaTokenizer



def load_llam():
    model_dir = os.path.join('llama', "original")

    model = LlamaForCausalLM.from_pretrained(model_dir)
    tokenizer = LlamaTokenizer.from_pretrained(model_dir)
    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.float16,
        device_map="auto",
        )
    return pipeline

def use_llama(pipeline,tokenizer, prompt):
    sequences = pipeline(
    prompt,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    max_length=400,
    )
    for seq in sequences:

        print(f"{seq['generated_text']}")
    