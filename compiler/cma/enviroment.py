next_addr = 0

def new_addr(size: int) -> int:
    global next_addr
    curr_addr = next_addr
    next_addr += size
    return curr_addr

def total_size(env: dict) -> int:
    return sum(map(lambda v: v['size'] , env.values()))

def global_variables(env: dict) -> dict:
    return dict(filter(lambda e: e[1]['scope'] == 'global', root(env).items()))

def root(env: dict) -> dict:
    while '..' in env:
        env = env['..']
    return env

def getitem(env: dict, key: any) -> any:
    # TODO: use this when cma calls dict.getitem()
    if key in env:
        return env[key]
    root_env = root(env)
    if key in root_env:
        return root_env[key]
    raise KeyError(f'No value {key} found in {env}')