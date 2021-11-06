from django.db.models import Model


class EntityStorage:
    entities: dict[str, Model] = {}

    def add(self, name, entity):
        self.entities[name] = entity
        setattr(self, name, entity)
