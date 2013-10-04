# -*- coding: utf8 -*-

__all__=['behave_as', 'can_substitute', 'subtypeof', 'append_sys_path']


def behave_as(*bases):
    dynamic_bases = __load_bases(bases)

    class Liskov(type):
        def __new__(cls, name, bases, attrs):
            return type.__new__(cls, name, dynamic_bases + bases, attrs)

    return Liskov

def subtypeof(base):
    mod_name, sep, cls_name = base.rpartition('.')
    module = __import__(mod_name, globals(), locals(), [cls_name])
    return getattr(module, cls_name)


def can_substitute(*bases):
    dynamic_bases = __load_bases(bases)

    def liskov(cls):
        bases = (cls, ) + dynamic_bases + cls.__bases__
        attrs = dict(cls.__dict__)
        return type(cls.__name__, bases, attrs)

    return liskov

def append_sys_path(path):
    import sys, os
    if os.path.isfile(path):
        path = os.path.dirname(path)

    sys.path.append(os.path.realpath(path))

def __load_bases(bases):
    dynamic_bases = tuple()
    for base in bases:
        cls = subtypeof(base)
        if cls not in dynamic_bases:
            dynamic_bases+= (cls, )
    return dynamic_bases

