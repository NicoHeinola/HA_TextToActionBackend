import json
from typing import List
from db_models.setting import Setting
from helpers.setting.dynamic_type_converter import DynamicTypeConverter
from .seeder import Seeder


class SettingSeeder(Seeder):
    def seed(self, replace: bool = False, keys_to_seed: List[str] = [], json_path="seeders/data/default_settings.json"):
        with open(json_path, "r", encoding="utf-8") as f:
            settings = json.load(f)

        for setting in settings:
            # Convert the value to string for storage
            setting["value"] = DynamicTypeConverter.to_string(setting["value"])

            if len(keys_to_seed) > 0 and setting["key"] not in keys_to_seed:
                continue

            existing = self.db.query(Setting).filter(Setting.key == setting["key"]).first()
            if existing:
                if not replace:
                    continue

                existing.value = setting["value"]
                existing.type = setting["type"]
            else:
                self.db.add(Setting(**setting))

        self.db.commit()
