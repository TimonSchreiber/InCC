def parent(env: dict) -> dict:
    if '..' in env:
        return env['..']
    else:
        None

def root(env: dict) -> dict:
    if parent(env):
        return root(parent(env))
    else:
        env

def lookup(env: dict, key1: str, key2: str) -> any:
    if key1 in env and key2 in env[key1]:
        return env[key1][key2]
    elif parent(env):
        return lookup(env[parent(env)], key1, key2)
    raise Exception(f'lookup of {key1},{key2} failed')

label_counter = 0
def label() -> int:
   global label_counter
   label_counter += 1
   return label_counter

global_addr = 0
def new_addr(size: int = 8) -> int:
    global global_addr
    curr_addr = global_addr
    global_addr+=size
    return curr_addr

def global_vars(env: dict) -> dict:
    return {x: env[x] for x in env if 'scope' in env[x] and env[x]['scope'] == 'global'}
def local_vars(env: dict) -> dict:
    return {x: env[x] for x in env if 'scope' in env[x] and env[x]['scope'] == 'local'}
def formal_vars(env: dict) -> dict:
    return {x: env[x] for x in env if 'scope' in env[x] and env[x]['scope'] == 'formal'}

def total_size(env):
    return sum([env[x]['size'] for x in env])
