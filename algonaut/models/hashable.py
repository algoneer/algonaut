from algonaut.utils.hashing import get_hash


class Hashable:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hash = get_hash(self.hash_data(kwargs))
