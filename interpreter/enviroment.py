def find_dict_for(d, key):
    if key in d:
        return d
    elif '..' in d and d['..'] is not None:
        return find_dict_for(d['..'], key)
    else:
        return None


class Enviroment(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locked_variables = set()

    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        elif '..' in self and self['..'] is not None:
            return self['..'][key]
        else:
            raise Exception(f'accessing undefined variable {key} in enviroment {self}')

    def __setitem__(self, key, value):
        if (key in self.locked_variables):
            # print(f'changing locked variable {key} in enviroment {self}')
            pass    ## also possible print message or raise Exception
        d = find_dict_for(self, key)
        if d is None:
            d = self
        dict.__setitem__(d, key, value)

    def set_parent(self, parent):
        dict.__setitem__(self, '..', parent)

    def get_parent(self):
        if '..' in self and self['..'] is not None:
            return self['..']
        else:
            return None

    def get_root(self):
        if '..' not in self:
            return self
        else:
            return self['..'].get_root()

    def lock_variable(self, key):
        self.locked_variables.add(key)

    def unlock_variable(self, key):
        self.locked_variables.remove(key)
