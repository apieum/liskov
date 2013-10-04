# -*- coding: utf8 -*-

__all__=['behave_as', 'can_substitute', 'subtypeof', 'append_sys_path', 'without']


def behave_as(*bases):
    substitute_bases = __load_bases(bases)

    class Liskov(type):
        def __new__(cls, name, bases, attrs):
            return type.__new__(cls, name, substitute_bases + bases, attrs)

    return Liskov

def subtypeof(base):
    mod_name, sep, cls_name = base.rpartition('.')
    module = __import__(mod_name, globals(), locals(), [cls_name])
    return getattr(module, cls_name)


def can_substitute(*bases):
    substitute_bases = __load_bases(bases)

    def liskov(cls, substitute_bases=substitute_bases):
        if hasattr(cls, 'constrained_subtype'):
            behaviours = cls.constrained_subtype
            new_bases = tuple()
            for base in substitute_bases:
                attrs = dict([
                    (key, value) for key, value in list(base.__dict__.items())
                    if key not in behaviours
                ])
                new_bases += (type(base.__name__, base.__bases__, attrs), )
            substitute_bases = new_bases

        bases = (cls, ) + substitute_bases + cls.__bases__
        attrs = dict(cls.__dict__)
        attrs['substitute_bases'] = substitute_bases
        return type(cls.__name__, bases, attrs)

    return liskov

def append_sys_path(path):
    import sys, os
    if os.path.isfile(path):
        path = os.path.dirname(path)

    sys.path.append(os.path.realpath(path))

def __load_bases(bases):
    substitute_bases = tuple()
    for base in bases:
        cls = subtypeof(base)
        if cls not in substitute_bases:
            substitute_bases+= (cls, )
    return substitute_bases

def without(*behaviours):
    def constraints(cls):
        setattr(cls, 'constrained_subtype', behaviours)
        return cls
    return constraints
