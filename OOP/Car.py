class Car:
    def __init__(self, horn, color, engine):
        self.horn = horn
        self.color = color
        self.engine = engine

    def __str__(self):
        return f"car's engine is {self.engine} and color is {self.color}"

    def pressHorn(self):
        print(f"{self.horn}")
