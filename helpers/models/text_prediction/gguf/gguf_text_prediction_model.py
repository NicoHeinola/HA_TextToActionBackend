import logging
import sys
from typing import List, Generator
from helpers.models.text_prediction.text_prediction_model import TextPredictionModel
from llama_cpp import Llama
import threading

logger = logging.getLogger(__name__)


class GGUFTextPredictionModel(TextPredictionModel):
    def __init__(self, model_name: str, *args, **kwargs):
        super().__init__(model_name)

        self._max_tokens: int = kwargs.get("max_tokens", 128)
        self._n_batch: int = kwargs.get("n_batch", 512 * 4)
        self._n_ctx: int = kwargs.get("n_ctx", 1024 * 2)

        self._model_folder: str = "gguf"
        self._model: Llama | None = self.load_model()

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
        )

        return model

    def _stream_prediction(self, tokens: List[int]) -> Generator:
        """Generator function that yields completion chunks from the model."""

        if not self._model:
            raise RuntimeError("Model is not loaded.")

        try:
            # Stream chunks as they're generated
            output = self._model.create_completion(
                tokens,
                stream=True,
                max_tokens=self._max_tokens,
                temperature=0.0,
                stop=['```"', "```\n", "}\n", "<|Assistant|>", "<|User|>"],
            )

            for chunk in output:
                yield chunk
        except Exception as e:
            logger.error("Error during prediction", exc_info=e)
            yield None

    def predict(self, system_prompt: str, user_input: str, timeout: float = 5.0) -> str:
        if not self._model:
            raise RuntimeError("Model is not loaded.")

        prompt = self._get_prompt_text(system_prompt, user_input)

        tokens: List[int] = self._model.tokenize(prompt.encode("utf-8"))

        result_container: dict = {"text": ""}
        thread: threading.Thread | None = None

        def _predict_in_thread():
            try:
                parsed_text: str = ""

                # Process each chunk from the generator
                for chunk in self._stream_prediction(tokens):
                    if thread is None:
                        return  # Thread was terminated due to timeout

                    if chunk is None:
                        continue

                    choices: list = chunk.get("choices", [])
                    if not choices:
                        continue

                    raw_text = choices[0].get("text", "")
                    parsed_text += raw_text

                result_container["text"] = parsed_text
            except Exception as e:
                logger.error("Error consuming generator", exc_info=e)

        # Start prediction in background thread
        thread = threading.Thread(target=_predict_in_thread, daemon=True)
        thread.start()
        thread.join(timeout=timeout)

        # Check if thread is still alive (timeout occurred)
        if thread.is_alive():
            thread = None
            logger.error("Prediction timed out after %.1f seconds", timeout)

        return result_container["text"].strip()
