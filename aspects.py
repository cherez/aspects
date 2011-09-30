import functools
def wrapper(func):
    def inner(*args):
        return inner.wrapped(*args)
    inner.wrapped = func
    return inner

def instance_wrapper(func, self):
    def inner(*args):
        return inner.wrapped(self, *args)
    inner.wrapped = func
    return inner

def replace_function(old, advice):
    name = old.__name__
    new = advice(old)
    functools.update_wrapper(new, old)
    if hasattr(old, 'im_class'): #this is from a class
        new.im_class = old.im_class
        new.im_self = old.im_self
        if old.im_self: #this is from an instance of the class
            #redefine new here, so that the last element doesn't
            #have an implicit self
            new = advice(old.im_func)
            functools.update_wrapper(new, old)
            setattr(old.im_self, name, instance_wrapper(new, old.im_self))
        else:
            setattr(old.im_class, name, wrapper(new))
    else:
        m = __import__(old.__module__)
        setattr(m, name, wrapper(new))

def wrap_function(func, advice):
    if hasattr(func, 'wrapped'):
        new = advice(func.wrapped)
        functools.update_wrapper(new, func.wrapped)
        func.wrapped = new
        return True

    replace_function(func, advice)
