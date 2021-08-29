class EntityStorage:
    entities = {}

    def add(self, name, entity):
        self.entities[name] = entity
        setattr(self, name, entity)
