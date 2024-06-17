def find_dict_for(d, key):
    if key in d:
        return d
    if d.parent is not None:
        return find_dict_for(d.parent, key)
        # return find_dict_for(d.get_parent(), key)
    return None


class Enviroment(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locked_variables = {'.', '..'}# set()
        self.parent: Enviroment = None

    def __getitem__(self, key):
        # if type(key) is int or key.isdigit():
        #     return int(key)
        if key in self:
            return dict.__getitem__(self, key)
        if self.parent:
            return self.parent[key]
        raise Exception(f'accessing undefined variable {key} in enviroment {self}')

    def __setitem__(self, key, value):
        if (key in self.locked_variables):
            raise Exception(f'changing locked variable {key} in enviroment {self}')
        d = find_dict_for(self, key)
        if d is None:
            d = self
        dict.__setitem__(d, key, value)

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def get_vals(self):
        """
        self.items()    -> List of (key, value) tuples of THIS dict (no parent)
        dict(...)       -> convert back to dict
        Enviroment(...) -> convert to Enviroment
        """
        return Enviroment(dict(self.items()))

    def __str__(self):
        if self.parent:
            return str(self.parent) + dict.__str__(self)
        else:
            return dict.__str__(self)

    def lock_variable(self, key):
        self.locked_variables.add(key)

    def unlock_variable(self, key):
        self.locked_variables.remove(key)
