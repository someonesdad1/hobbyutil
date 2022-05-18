'''
A dictionary that is an invertible function
    Keys and values must be unique in "both directions".  Call the instance
    as if it were a function to go in the reverse direction.
 
    Here's how to initialize from a dict:
        categories = bidict()
        categories.update(
            {
                'all':      0,
                'gas':      1,
                'liquid':   2,
                'metal':    3,
                'mineral':  4,
                'misc':     5,
                'plastic':  6,
                'wood':     7,
            }
        )
 
    Then
        categories["metal"] returns 3
        categories(3) returns "metal"
 
    Use categories.invert() to get a new bidict object where the inverse
    mapping is the "forward" mapping.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2009, 2011, 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> A dictionary that is an invertible function.  As
    # long as the mapping is one-to-one, you can use the dictionary in
    # either direction.  dict[a] goes the "normal" direction and dict(a)
    # goes the reverse direction.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
class bidict(dict):
    def __init__(self, *p, **kw):
        # Implementation:  keep the inverse mapping in self._inv.
        self.super = super(bidict, self)
        self.super.__init__(*p, **kw)
        self._inv = {}
        self._frozen = kw.get("frozen", False)
        # Construct the inverse mapping
        for key in self:
            value = self[key]
            try:
                if value in self._inv:
                    raise ValueError("'%s' is a duplicate value" % value)
            except TypeError as e:
                # Probably a mutable object
                raise TypeError("Can't put '%s' into a bidict" % value)
            self._inv[value] = key
    def __setitem__(self, key, value):
        self._check()
        if value in self._inv:
            raise ValueError("'%s' is duplicate value" % value)
        self.super.__setitem__(key, value)
        self._inv[value] = key
    def __delitem__(self, key):
        self._check()
        value = self[key]
        self.super.__delitem__(key)
        del self._inv[value]
    def __call__(self, value):
        'Return the key that corresponds to value.'
        return self._inv[value]
    def _check(self):
        if self._frozen:
            raise ValueError("bidict is frozen")
    def clear(self):
        self._check()
        self.super.clear()
        self._inv.clear()
    def invert(self):
        '''Return a new bidict object that has the dictionaries
        reversed.
        '''
        b = bidict(self._inv)
        b._inv = dict(self)
        return b
    def pop(self, key, default=None):
        self._check()
        if key in self:
            value = self.super.pop(key)
            del self._inv[value]
            return value
        if default is None:
            raise KeyError("No entry for key '%s'" % key)
        else:
            return default
    def popitem(self):
        self._check()
        key, value = self.super.popitem()
        del self._inv[value]
        return key, value
    def copy(self):
        b = bidict()
        b.super.update(self.super.copy())
        b._inv = self._inv.copy()
        return b
    def setdefault(self, key, default=None):
        self._check()
        if key not in self:
            self[key] = default
        return self[key]
    def update(self, *p, **kw):
        self._check()
        if p:
            if len(p) != 1:
                raise ValueError("Only one parameter allowed")
            if kw:
                msg = "Keyword parameters not allowed with a parameter"
                raise ValueError(msg)
            items = p[0].items() if isinstance(p[0], dict) else p[0]
        elif kw:
            items = kw.items()
        else:
            raise ValueError("Need a parameter or keyword arguments")
        for key, value in items:
            if value in self:
                raise ValueError("'%s' is a duplicate value" % value)
            self[key] = value
            self._inv[value] = key
    def __str__(self):
        return ''.join(("bidict", self.super.__str__()))
    def _set_frozen(self, frozen):
        self._frozen = bool(frozen)
    def _get_frozen(self, frozen):
        return self._frozen
    frozen = property(_get_frozen, _set_frozen)
# Convenience instance that maps month names to number and vice versa
months = bidict(zip("jan feb mar apr may jun jul aug sep oct nov dec".split(),
                    range(1, 13)))
if __name__ == "__main__": 
    from lwtest import run, assert_equal, raises
    from pdb import set_trace as xx
    def init():
        keys, values   = ["jan", "feb"], [1, 2]
        d = dict(zip(keys, values))
        bd = bidict(d)
        Check(bd, keys, values)
        return keys, values, bd
    def Check(bd, keys, values):
        assert(isinstance(bd, bidict))
        for i in bd:
            assert(i in keys)
        for i in bd.values():
            assert(i in values)
        assert(set(bd.keys()) == set(bd._inv.values()))
        assert(set(bd.values()) == set(bd._inv.keys()))
    def TestLookup():
        keys, values, bd = init()
        assert(bd["jan"] == 1)
        assert(bd(1) == "jan")
    def TestKeysAndValues():
        keys, values, bd = init()
        assert(set(values) == set(bd.values()))
        assert(set(keys) == set(bd.keys()))
    def TestAddDeleteNewValue():
        keys, values, bd = init()
        bd["mar"] = 3
        keys.append("mar")
        values.append(3)
        Check(bd, keys, values)
        # Show we can delete it
        del bd["mar"]
        del keys[-1]
        del values[-1]
        Check(bd, keys, values)
    def TestSwapDictionaries():
        keys, values, bd = init()
        rev_bd = bd.invert()
        Check(rev_bd, values, keys)
    def TestMethods():
        keys, values, bd = init()
        assert(set(bd.items()) == set(zip(keys, values)))
        assert("jan" in bd)
        assert(bd.get("xyz", 88) == 88)
        assert(bd.get("jan", None) == 1)
        b2 = bd.copy()
        assert(bd == b2) # Can be tested for equality
        b2.clear()
        assert(not len(b2))
        b2 = bd.copy()
        assert(b2.setdefault("jun", 89) == 89)
        assert(b2.setdefault("jun") == 89)
        #assert(set(bd.iterkeys()) == set(bd.keys()))
        #assert(set(bd.itervalues()) == set(bd.values()))
        value = b2.pop("jun")
        assert(value == 89)
        # Get exception on empty pops
        raises(KeyError, b2.pop, "xyz")
        raises(KeyError, b2.pop, "jun")
        # Show default value for pop works
        value = b2.pop("jun", 91)
        assert(value == 91)
        key, value = b2.popitem()
        assert(len(b2) == 1)
        # Get ValueError exception for a duplicate value
        raises(ValueError, bd.__setitem__, "xyz", 2)
        # Get key error for accessing nonexistent key
        raises(KeyError, b2.__getitem__, "xyz")
        # Get key error for accessing nonexistent value
        raises(KeyError, b2, 1000)
    def TestCannotUseMutableObject():
        keys, values, bd = init()
        d = dict([("jan", [1])])
        raises(TypeError, bidict, d)
        # OK to use a tuple
        d = dict([("jan", (1,))])
        bidict(d)
    def TestUpdate():
        keys, values, bd = init()
        # Update with dict
        d = {"new":24}
        bd.update(d)
        assert(bd["new"] == 24)
        assert(bd(24) == "new")
        # Update with key/value pair iterable
        keys, values, bd = init()
        d = [("new", 24)]
        bd.update(d)
        assert(bd["new"] == 24)
        assert(bd(24) == "new")
        # Update with keywords
        keys, values, bd = init()
        bd.update(new=24)
        assert(bd["new"] == 24)
        assert(bd(24) == "new")
        # TypeError if update with mutable
        keys, values, bd = init()
        d = {"new" : [1, 2]}
        raises(TypeError, bd.update, d)
    def TestFrozen():
        keys, values, bd = init()
        bd.frozen = True
        with raises(ValueError):
            del bd["jan"]
    exit(run(globals())[0])
