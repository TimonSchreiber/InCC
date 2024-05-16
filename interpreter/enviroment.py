def find_dict_for(d, key):
    if key in d:
        return d
    elif '..' in d and d['..'] is not None:
        return find_dict_for(d['..'], key)
    else:
        return None


class Enviroment(dict):
    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        elif '..' in self and self['..'] is not None:
            return self['..'][key]
        else:
            raise Exception(f'accessing undefined variable {key} in enviroment {self}')

    def __setitem__(self, k, v):
        d = find_dict_for(self, k)
        if d is None:
            d = self
        dict.__setitem__(d, k, v)

    def set_parent(self, p):
        dict.__setitem__(self, '..', p)

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
