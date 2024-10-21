next_addr = 0

def new_addr(size: int) -> int:
    global next_addr
    tmp = next_addr
    next_addr += size
    return tmp

def total_size(env: dict) -> int:
    return sum(map(lambda v: v['size'] , env.values()))

def global_variables(env: dict) -> dict:
    return dict(filter(lambda e: e[1]['scope'] == 'global', env.items()))
