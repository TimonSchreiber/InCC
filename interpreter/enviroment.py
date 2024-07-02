from typing import Self

class Enviroment(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locked_variables = set()
        self.parent: Enviroment = None
        self.surrounding_struct: Enviroment = None

    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        if self.parent:
            return self.parent[key]
        raise Exception(f'accessing undefined variable {key} in enviroment {self}')

    def __setitem__(self, key, value):
        env = find_env_for(self, key)
        if env is None:
            env = self
        if key in env.locked_variables:
            print(f'not changing locked variable {key} in enviroment {env}')
            # Not sure if print is enough or an exception should be raised
            return
        dict.__setitem__(env, key, value)

    def set_parent(self, parent):
        self.parent = parent

    # def get_parent(self) -> Self:
    #     return self.parent

    # def get_vals(self) -> Self:
    #     """
    #     self.items()    -> List of (key, value) tuples of THIS dict (no parent)
    #     dict(...)       -> convert back to dict
    #     Enviroment(...) -> convert to Enviroment
    #     """
    #     env = Enviroment(dict(self.items()))
    #     env.locked_variables = set(self.locked_variables)
    #     return env

    def get_item(self, dots: int, key):
        env = get_parent_env(self, dots, key)
        if env is not None:
            return env[key]
        raise Exception(f'Inheritance hirachy has not enough layers.')

    def remove_root(self):
        if self.parent is None:
            return #self
        env: Self = self
        while env.parent.parent is not None:
            env = env.parent
        env.parent = None
        return #self

    def add_root(self, root: Self) -> None:
        env: Self = self
        while env.parent is not None:
            env = env.parent
        env.parent = root

    def lock_variables(self, keys):
        for key in keys : self.locked_variables.add(key)

    def unlock_variables(self, keys):
        for key in keys : self.locked_variables.remove(key)

    def __str__(self) -> str:
        if self.parent:
            return dict.__str__(self) + str(self.parent)
        else:
            return dict.__str__(self)

## ---------- END OF CLASS ENVIROMENT ----------

def find_env_for(env: Enviroment, key) -> Enviroment:
    if key in env:
        return env
    if env.parent is not None:
        return find_env_for(env.parent, key)
    return None

def get_parent_env(env: Enviroment, dots: int, key) -> Enviroment:
    if dots <= 1:
        return env
    if env.parent is not None:
        return get_parent_env(env.parent, dots-1, key)
    return None
