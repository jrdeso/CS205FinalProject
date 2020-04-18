class EntityPoint2D:
    def __init__(self, x, y, entities=None):
        self.coords = (x, y)
        self.entities = entities or []

    def __len__(self):
        return len(self.coords)

    def __getitem__(self, i):
        return self.coords[i]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"[{self.coords[0]}, {self.coords[1]}] {self.entities}"
