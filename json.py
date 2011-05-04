def json(obj):
    """A simple compact JSON formatter.

    The main purpose of this was to encode a subset of the possible
    JSON objects simply and as compactly as possible. Floats, for
    instance, are rounded to at most 8 decimal places, which gives
    some savings for inexact representations like 15.499999999999999.

    Strings are most likely _not_ handled correctly in general, but it
    is a simple matter to use json.dumps() to replace that part (I'm
    keeping this as it is for self-sufficiency).
    """
    def format_json(x):
        return {
            type(None) : lambda x: 'null',
            bool       : lambda x: str(x).lower(),
            str        : lambda x: '"%s"' % x,
            float      : lambda x: "%.8g" % x,
            np.float64 : lambda x: "%.8g" % x,
            list       : lambda x: "[%s]" %
            ','.join(map(format_json, x)),
            dict       : lambda x: "{%s}" %
            ','.join( '"%s":%s'%(k,format_json(v))
                      for k,v in x.items() ),
            }.get(type(x), lambda x: str(x))(x)
    return format_json( obj )

