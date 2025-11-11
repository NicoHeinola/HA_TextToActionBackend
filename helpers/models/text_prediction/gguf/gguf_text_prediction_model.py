from helpers.models.text_prediction.text_prediction_model import TextPredictionModel
from llama_cpp import Llama


class GGUFTextPredictionModel(TextPredictionModel):
    def __init__(self, model_name: str, system_prompt: str = "", *args, **kwargs):
        super().__init__(model_name, system_prompt)

        self._model_folder: str = "gguf"
        self._model: Llama = self.load_model()

        self._max_tokens: int = kwargs.get("max_tokens", 128)

    def load_model(self) -> Llama:
        model: Llama = Llama(
            model_path=self.model_path,
            n_ctx=2048,
            n_gpu_layers=-1,  # offload all layers
            n_threads=1,  # only used for tokenization
            offload_kv=True,  # move KV cache to GPU
            use_mlock=False,
            verbose=False,
        )

        return model

    def predict(self, text: str) -> str:
        prompt = self._get_prompt_text(text)

        model: Llama = self._model
        output = model(prompt, max_tokens=self._max_tokens, temperature=0.0, stop=["<|User|>", "<|User|}>"])

        if not isinstance(output, dict):
            return ""

        choices: list = output.get("choices", [])
        raw_text = choices[0].get("text")
        return raw_text.strip()
