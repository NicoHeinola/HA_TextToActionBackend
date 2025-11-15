from typing import List
from helpers.models.text_prediction.text_prediction_model import TextPredictionModel
from llama_cpp import Llama


class GGUFTextPredictionModel(TextPredictionModel):
    def __init__(self, model_name: str, system_prompt: str = "", *args, **kwargs):
        super().__init__(model_name, system_prompt)

        self._max_tokens: int = kwargs.get("max_tokens", 128)
        self._n_batch: int = kwargs.get("n_batch", 512 * 4)
        self._n_ctx: int = kwargs.get("n_ctx", 1024 * 2)

        self._model_folder: str = "gguf"
        self._model: Llama = self.load_model()

    def load_model(self) -> Llama:
        model: Llama = Llama(
            model_path=self.model_path,
            n_ctx=self._n_ctx,
            # PERFORMANCE TUNING
            n_gpu_layers=-1,  # Move all layers to GPU
            flash_attn=True,  # FLASH ATTENTION (huge boost)
            n_threads=4,  # Faster tokenization (CPU side)
            tensor_split=None,  # Single GPU
            verbose=False,
            n_batch=self._n_batch,
            # OTHER
            seed=-1,  # Use random seed
        )

        return model

    def predict(self, text: str) -> str:
        prompt = self._get_prompt_text(text)

        tokens: List[int] = self._model.tokenize(prompt.encode("utf-8"))
        output = self._model.create_completion(
            tokens,
            max_tokens=self._max_tokens,
            temperature=0.0,
            stop=['```"', "```\n", "}\n", "<|Assistant|>", "<|User|>"],
        )

        if not isinstance(output, dict):
            return ""

        choices: list = output.get("choices", [])
        raw_text = choices[0].get("text")

        return raw_text.strip()
