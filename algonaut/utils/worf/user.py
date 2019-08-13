class User:
    def __init__(self, d):
        self.d = d

    @property
    def roles(self):
        return self.d.get("roles", [])
