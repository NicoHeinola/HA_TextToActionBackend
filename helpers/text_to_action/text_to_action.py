import json
import logging
from typing import List
from db_models.action import Action
from helpers.models.text_prediction.text_prediction_model import TextPredictionModel


logger = logging.getLogger(__name__)


class TextToAction:
    def __init__(self, model: TextPredictionModel) -> None:
        self._model: TextPredictionModel = model

    def convert_text_to_action(self, text: str) -> dict:
        prediction: str = self._model.predict(text)

        # Filter out the prediction to extract JSON content
        # Remove everything before ```json
        if "```json" in prediction:
            prediction = prediction.split("```json", 1)[1].strip()

        # Remove everything after the closing ```
        if "```" in prediction:
            prediction = prediction.split("```", 1)[0].strip()

        # Try to convert prediction to JSON
        try:
            prediction_json = json.loads(prediction)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse prediction as JSON: {e}")
            prediction_json = {}

        return prediction_json
