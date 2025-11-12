import json
from db_models.setting import Setting
from .seeder import Seeder


class SettingSeeder(Seeder):
    def seed(self, replace: bool = False, json_path="seeders/data/default_settings.json"):
        with open(json_path, "r", encoding="utf-8") as f:
            settings = json.load(f)

        for setting in settings:
            existing = self.db.query(Setting).filter(Setting.key == setting["key"]).first()
            if existing:
                if not replace:
                    continue

                existing.value = setting["value"]
                existing.type = setting["type"]
            else:
                self.db.add(Setting(**setting))

        self.db.commit()
