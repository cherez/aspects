def replace_function(old, new):
    name = old.__name__
    new.__name__ = name
    if hasattr(old, 'im_class'): #this is from a class
        new.im_class = old.im_class
        setattr(old.im_class, name, new)
    elif hasattr(old, 'func_globals'):
        old.func_globals[name] = new
    else:
        m = __import__(old.__module__)
        setattr(m, name, new)

def wrap_function(func, advice):
    new = advice(func)
    replace_function(func, new)
