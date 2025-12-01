import json


class DynamicTypeConverter:
    @staticmethod
    def to_type(value, target_type):
        if target_type == "string":
            return str(value)
        elif target_type == "integer":
            return int(value)
        elif target_type == "float":
            return float(value)
        elif target_type == "boolean":
            return bool(value)
        elif target_type == "array":
            return json.loads(value) if isinstance(value, str) else list(value)
        elif target_type == "object":
            return json.loads(value) if isinstance(value, str) else dict(value)

    @staticmethod
    def to_string(value):
        if isinstance(value, (list, dict)):
            return json.dumps(value)

        return str(value)
