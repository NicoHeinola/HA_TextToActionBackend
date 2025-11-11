from abc import ABC, abstractmethod
import os
from typing import Any


class TextPredictionModel(ABC):
    def __init__(self, model_name: str, system_prompt: str = ""):
        self._model_name = model_name
        self._system_prompt = system_prompt

        # Used for getting model path
        self._model_folder: str = ""

    @property
    def model_path(self) -> str:
        if os.path.exists(self._model_name):
            return self._model_name

        model_path: str = os.path.join("models", "text_prediction", self._model_folder, self._model_name)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at path: {model_path}")

        return model_path

    def _get_prompt_text(self, user_input: str) -> str:
        return '<|System|>"{system_prompt}"\n<|User|>"{user_input}"\n<|Assistant|>"'.format(
            system_prompt=self._system_prompt, user_input=user_input
        )

    @abstractmethod
    def load_model(self) -> Any:
        pass

    @abstractmethod
    def predict(self, text: str) -> str:
        pass
