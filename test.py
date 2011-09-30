import aspects

def t():
    return 1

def test_global():
    def inc(func):
        def inner():
            return func() + 1
        return inner

    if t() != 1:
        return False
    aspects.wrap_function(t, inc)
    if t() != 2:
        return False

    return True

def test_class():
    class C:
        def t(self):
            return 1

    def inc(func):
        def inner(self):
            return func(self) + 1
        return inner

    c = C()

    if c.t() != 1:
        return False
    aspects.wrap_function(C.t, inc)
    c = C()
    if c.t() != 2:
        return False

    return True

def test_instance():
    class C:
        def t(self):
            return 1

    def inc(func):
        def inner(self):
            return func(self) + 1
        return inner

    c = C()
    if c.t() != 1:
        return False
    aspects.wrap_function(c.t, inc)
    if c.t() != 2:
        return False
    c = C()
    if c.t() != 1:
        return False
    return True

def test_nested():
    @aspects.wrapper
    def t():
        return 1
    def inc(func):
        def inner():
            return func() + 1
        return inner
    for i in range(1, 10):
        if t() != i:
            return False
        aspects.wrap_function(t, inc)
    return True


def test():
    tests = [
            test_global,
            test_class,
            test_instance,
            test_nested,
            ]
    successes = 0
    for test in tests:
        if test():
            successes += 1
        else:
            print 'Failed ', test.__name__
    print('%s succeeded out of %s' % (successes, len(tests)))

if __name__ == '__main__':
    test()
