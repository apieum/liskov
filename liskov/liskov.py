# -*- coding: utf8 -*-

__all__=['behave_as', 'can_substitute', 'subtypeof', 'append_sys_path', 'apart_from']


def behave_as(*bases):
    substitute_bases = __load_bases(bases)

    class Liskov(type):
        constraints = tuple()
        def __new__(cls, name, bases, attrs):
            new_bases = _remove_behaviours(substitute_bases, cls.constraints)
            return type.__new__(cls, name, new_bases + bases, attrs)

        @classmethod
        def apart_from(cls, *behaviours):
            cls.constraints = behaviours
            return cls

    return Liskov

def subtypeof(base):
    mod_name, sep, cls_name = base.rpartition('.')
    module = __import__(mod_name, globals(), locals(), [cls_name])
    return getattr(module, cls_name)

def _remove_behaviours(bases, behaviours):
    new_bases = tuple()
    for base in bases:
        base_attrs = base.__dict__
        attrs = dict([
            (key, value) for key, value in base_attrs.items()
            if key not in behaviours
        ])
        if len(base_attrs) > len(attrs):
            base = type(base.__name__, base.__bases__, attrs)
        new_bases += (base, )
    return new_bases

def can_substitute(*bases):
    substitute_bases = __load_bases(bases)

    def liskov(cls, substitute_bases=substitute_bases):
        if hasattr(cls, 'constrained_subtype'):
            substitute_bases = _remove_behaviours(substitute_bases, cls.constrained_subtype)

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

def apart_from(*behaviours):
    def constraints(cls):
        setattr(cls, 'constrained_subtype', behaviours)
        return cls
    return constraints
