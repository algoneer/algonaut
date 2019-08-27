import hashlib


class Hasher(object):
    def __init__(self):
        self.digest = hashlib.md5()

    def add(self, value):
        if isinstance(value, str):
            v = value.encode("utf-8", "ignore")
        elif isinstance(value, (bytes)):
            v = str(value, errors="replace").encode("utf-8", "ignore")
        elif isinstance(value, (int, float, complex, bool)):
            v = str(bytes(value), errors="replace").encode("utf-8", "ignore")
        elif isinstance(value, (tuple, list)):
            for v in value:
                self.add(v)
            return
        elif isinstance(value, dict):
            for key, v in sorted(value.items(), key=lambda x: x[0]):
                self.add(key)
                self.add(v)
            return
        elif value is None:
            v = b"1bcdadabdf0de99dbdb747e951e967c5"
        else:
            raise AttributeError("Unhashable type: %s" % bytes(type(value)))

        self.digest.update(v)

    def digest(self):
        return self.digest


def get_hash(node, fields=None, exclude=[]):
    """
    Here we generate a unique hash for a given node in the syntax tree.
    """

    hasher = Hasher()

    def add_to_hash(value):

        if isinstance(value, dict):
            for key, v in sorted(value.items(), key=lambda x: x[0]):

                if (fields is not None and key not in fields) or (
                    exclude is not None and key in exclude
                ):
                    continue
                add_to_hash(key)
                add_to_hash(v)
        elif (
            isinstance(value, (tuple, list))
            and value
            and isinstance(value[0], (dict, node_class))
        ):
            for i, v in enumerate(value):
                hasher.add(i)
                add_to_hash(v)
        else:
            hasher.add(value)

    add_to_hash(node)

    return hasher.digest.digest()


class Hashable:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_hash()

    def generate_hash(self):
        self.hash = get_hash(self.hash_data())
