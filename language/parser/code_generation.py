_gen = None

def set_generator_module(m):
    global _gen
    _gen = m

def gen():
    return _gen

def generator_module_implements(used_procedures_and_classes): # check availability of module and all referenced items
    return all(hasattr(_gen, x) for x in used_procedures_and_classes)

def check_generator_module(used_procedures_and_classes):
    if not _gen:
        raise Exception("No code generator provided please use 'set_generator_module()' in parser module")
    if not generator_module_implements(used_procedures_and_classes):
        raise Exception("code generator doesn't implement all expected functions")