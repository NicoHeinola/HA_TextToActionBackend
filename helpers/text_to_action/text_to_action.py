import json
import logging
from typing import List
from db_models.action import Action
from helpers.models.text_prediction.text_prediction_model import TextPredictionModel


logger = logging.getLogger(__name__)


class TextToAction:
    def __init__(self, model: TextPredictionModel) -> None:
        self._model: TextPredictionModel = model

    def convert_text_to_action(self, text: str, **kwargs) -> dict:
        prediction: str = self._model.predict(text, **kwargs)

        logger.info(f"Raw model prediction: {prediction}")

        # Filter out the prediction to extract JSON content
        # Remove everything before ```json
        if "```json" in prediction:
            prediction = prediction.split("```json", 1)[1].strip()

        # Remove everything after the closing ```
        if "```" in prediction:
            prediction = prediction.split("```", 1)[0].strip()

        # Start the prediction from the first {
        first_brace_index = prediction.find("{")
        if first_brace_index != -1:
            prediction = prediction[first_brace_index:]

        # Try to fix common JSON issues
        prediction = prediction.strip("\n")
        prediction = prediction.replace('\\"', '"')
        prediction_before_modification: str = prediction

        if not prediction.startswith("{"):
            prediction = "{" + prediction

        if prediction.endswith('}"'):
            prediction = prediction[:-1]

        if not prediction.endswith(("}", "]")) and not prediction.endswith("{"):
            if not prediction.endswith('"'):
                prediction += '"'

            prediction += "}"

        # Fix bracket amounts at the end
        open_braces = prediction.count("{")
        close_braces = prediction.count("}")
        if close_braces < open_braces:
            prediction += "}" * (open_braces - close_braces)

        # Try to convert prediction to JSON
        try:
            logger.info(f"Raw prediction before JSON parsing: {prediction}")
            prediction_json = json.loads(prediction)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse prediction as JSON: {e}")
            prediction_json = {}

            # If answer contains a lot of \", it means we can't convert to text
            curly_count = prediction_before_modification.count("{")
            square_count = prediction_before_modification.count("[")
            quote_count = prediction_before_modification.count('"')

            if curly_count < 1 and square_count < 1 and quote_count < 5:
                prediction_json = {
                    "ai_answer": prediction_before_modification,
                }

        return prediction_json
