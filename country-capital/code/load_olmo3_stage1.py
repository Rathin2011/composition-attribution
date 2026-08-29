"""Load the final stage-one OLMo 3 7B checkpoint and run a smoke prompt."""

from __future__ import annotations

import argparse
import json


MODEL_ID = "allenai/Olmo-3-1025-7B"
STAGE_ONE_REVISION = "stage1-step1413814"
STAGE_ONE_COMMIT = "373bad25002f1624757a73235c5ca844c6375c25"
MODEL_DTYPE = "bfloat16"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", default="Language modeling is")
    parser.add_argument("--max-new-tokens", type=int, default=8)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=STAGE_ONE_COMMIT)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        revision=STAGE_ONE_COMMIT,
        device_map="auto",
        dtype=torch.bfloat16,
    )
    model.eval()

    inputs = tokenizer(args.prompt, return_tensors="pt", return_token_type_ids=False)
    input_device = model.get_input_embeddings().weight.device
    inputs = {name: tensor.to(input_device) for name, tensor in inputs.items()}

    with torch.inference_mode():
        output_ids = model.generate(
            **inputs,
            do_sample=False,
            max_new_tokens=args.max_new_tokens,
            pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
        )

    prompt_length = inputs["input_ids"].shape[1]
    completion = tokenizer.decode(output_ids[0, prompt_length:], skip_special_tokens=True)
    print(
        json.dumps(
            {
                "model": MODEL_ID,
                "stage_one_revision": STAGE_ONE_REVISION,
                "commit": STAGE_ONE_COMMIT,
                "dtype": MODEL_DTYPE,
                "prompt": args.prompt,
                "completion": completion,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
