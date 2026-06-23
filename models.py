# models.py

import gc
import re

import torch
from transformers import pipeline


MODELS = {
    "Gemma 1B": "google/gemma-3-1b-it",
    "Llama 3.2 1B": "meta-llama/Llama-3.2-1B",
    "Qwen 0.6B": "Qwen/Qwen3-0.6B",
}

PROMPT_TEMPLATE = """
Who is {name}?

Give a short factual description in one sentence.
"""


def load_pipeline(model_id: str):

    dtype = (
        torch.float16
        if torch.cuda.is_available()
        else torch.float32
    )

    return pipeline(
        task="text-generation",
        model=model_id,
        torch_dtype=dtype,
    )


def unload_pipeline(pipe):

    try:
        del pipe
    except Exception:
        pass

    gc.collect()

    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def clean_output(text: str):

    if not text:
        return ""

    text = text.strip()

    while True:

        cleaned = re.sub(
            r"^(answer|assistant|user|human)\s*:\s*",
            "",
            text,
            flags=re.IGNORECASE,
        ).strip()

        if cleaned == text:
            break

        text = cleaned

    text = re.sub(r"\s+", " ", text)

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    if sentences:
        return sentences[0].strip()

    return text.strip()


def query_model(model_name: str, person_name: str):

    model_id = MODELS[model_name]

    pipe = load_pipeline(model_id)

    prompt = PROMPT_TEMPLATE.format(
        name=person_name
    )

    try:

        output = pipe(
            prompt,
            max_new_tokens=120,
            do_sample=False,
            return_full_text=False,
        )

        text = output[0]["generated_text"]

        return clean_output(text)

    finally:

        unload_pipeline(pipe)


def run_all_models(person_name: str):

    results = {}

    for model_name in MODELS:

        try:

            results[model_name] = query_model(
                model_name,
                person_name,
            )

        except Exception as e:

            results[model_name] = (
                f"ERROR: {str(e)}"
            )

    return results