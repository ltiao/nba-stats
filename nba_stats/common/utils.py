"""
For reference:

>>> from datetime import timedelta, datetime
>>> from dateutil import relativedelta

>>> datetime(2003, 1, 1) + relativedelta.relativedelta(years=4)
datetime.datetime(2007, 1, 1, 0, 0)

>>> datetime(2003, 1, 1) + timedelta(days=365*4)
datetime.datetime(2006, 12, 31, 0, 0)

>>> datetime(2003, 1, 1) + 4 * relativedelta.relativedelta(years=1)
datetime.datetime(2007, 1, 1, 0, 0)

>>> relativedelta.relativedelta(years=-4) == -4 * relativedelta.relativedelta(years=1)
True

>>> datetime(2003, 1, 1) + relativedelta.relativedelta(years=-4)
datetime.datetime(1999, 1, 1, 0, 0)

>>> datetime(2003, 1, 1) -4 * relativedelta.relativedelta(years=1)
datetime.datetime(1999, 1, 1, 0, 0)

>>> datetime(2003, 1, 1) + 4 * timedelta(days=365)
datetime.datetime(2006, 12, 31, 0, 0)
"""

import datetime

from dateutil import relativedelta
from itertools import chain, islice

# TODO: Unit/regression testing
# TODO: Documentation

YEAR_DELTA = relativedelta.relativedelta(years=1)

def datetime_count(start, step=YEAR_DELTA):
    """
    >>> start = datetime.datetime(2003, 4, 4)

    >>> list(islice(datetime_count(start), 5)) #doctest: +NORMALIZE_WHITESPACE
    [datetime.datetime(2003, 4, 4, 0, 0), datetime.datetime(2004, 4, 4, 0, 0), 
    datetime.datetime(2005, 4, 4, 0, 0), datetime.datetime(2006, 4, 4, 0, 0), 
    datetime.datetime(2007, 4, 4, 0, 0)]

    >>> list(islice(datetime_count(start, -YEAR_DELTA), 5)) #doctest: +NORMALIZE_WHITESPACE
    [datetime.datetime(2003, 4, 4, 0, 0), datetime.datetime(2002, 4, 4, 0, 0), 
    datetime.datetime(2001, 4, 4, 0, 0), datetime.datetime(2000, 4, 4, 0, 0), 
    datetime.datetime(1999, 4, 4, 0, 0)]
    """
    current = start
    while True:
        yield current
        current += step

def datetime_range(start, stop, step):
    """
    >>> start = datetime.datetime(2013, 4, 4)
    >>> end = datetime.datetime(2013, 5, 2)

    >>> list(datetime_range(start, end, datetime.timedelta(days=5))) #doctest: +NORMALIZE_WHITESPACE
    [datetime.datetime(2013, 4, 4, 0, 0), datetime.datetime(2013, 4, 9, 0, 0), 
    datetime.datetime(2013, 4, 14, 0, 0), datetime.datetime(2013, 4, 19, 0, 0), 
    datetime.datetime(2013, 4, 24, 0, 0), datetime.datetime(2013, 4, 29, 0, 0)]

    >>> list(datetime_range(end, start, -datetime.timedelta(days=6))) #doctest: +NORMALIZE_WHITESPACE
    [datetime.datetime(2013, 5, 2, 0, 0), datetime.datetime(2013, 4, 26, 0, 0), 
    datetime.datetime(2013, 4, 20, 0, 0), datetime.datetime(2013, 4, 14, 0, 0), 
    datetime.datetime(2013, 4, 8, 0, 0)]

    >>> end = datetime.datetime(2016, 5, 2)
    >>> list(datetime_range(start, end, YEAR_DELTA)) #doctest: +NORMALIZE_WHITESPACE
    [datetime.datetime(2013, 4, 4, 0, 0), datetime.datetime(2014, 4, 4, 0, 0), 
    datetime.datetime(2015, 4, 4, 0, 0), datetime.datetime(2016, 4, 4, 0, 0)]

    >>> list(datetime_range(end, start, -datetime.timedelta(days=365))) #doctest: +NORMALIZE_WHITESPACE
    [datetime.datetime(2016, 5, 2, 0, 0), datetime.datetime(2015, 5, 3, 0, 0), 
    datetime.datetime(2014, 5, 3, 0, 0), datetime.datetime(2013, 5, 3, 0, 0)]

    >>> list(datetime_range(end, start, -YEAR_DELTA)) #doctest: +NORMALIZE_WHITESPACE
    [datetime.datetime(2016, 5, 2, 0, 0), datetime.datetime(2015, 5, 3, 0, 0), 
    datetime.datetime(2014, 5, 3, 0, 0), datetime.datetime(2013, 5, 3, 0, 0)]

    >>> list(datetime_range(end, start, datetime.timedelta(days=1))) #doctest: +NORMALIZE_WHITESPACE
    []

    >>> list(datetime_range(start, end, datetime.timedelta(days=-1))) #doctest: +NORMALIZE_WHITESPACE
    []

    >>> datetime_range(start, end, YEAR_DELTA) #doctest: +ELLIPSIS
    <generator object datetime_range at 0x...>

    """

    current = start
    if step.days < 0:
        cond = lambda current, stop: current >= stop
    else:
        cond = lambda current, stop: current < stop

    while cond(current, stop):
        yield current
        current += step

def strpyear(year_str):
    """
    >>> strpyear('2014')
    datetime.datetime(2014, 1, 1, 0, 0)

    >>> strpyear('14')
    datetime.datetime(2014, 1, 1, 0, 0)

    >>> strpyear('garbage') #doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: time data 'garbage' does not match format ...
    """

    try:
        return datetime.datetime.strptime(year_str, '%y')
    except ValueError:
        return datetime.datetime.strptime(year_str, '%Y')

def year_of_season(season, first=False):
    """
    >>> year_of_season('2014-15')
    datetime.datetime(2015, 1, 1, 0, 0)

    >>> year_of_season('2014-15', first=True)
    datetime.datetime(2014, 1, 1, 0, 0)

    >>> year_of_season('2014')
    datetime.datetime(2014, 1, 1, 0, 0)

    >>> year_of_season('2014', first=True)
    datetime.datetime(2014, 1, 1, 0, 0)

    >>> year_of_season(2014)
    datetime.datetime(2014, 1, 1, 0, 0)

    >>> year_of_season(2014, first=True)
    datetime.datetime(2014, 1, 1, 0, 0)

    >>> year_of_season('2012-2013')
    datetime.datetime(2013, 1, 1, 0, 0)

    >>> year_of_season('2012-2013', first=True)
    datetime.datetime(2012, 1, 1, 0, 0)

    >>> year_of_season('12-2013')
    datetime.datetime(2013, 1, 1, 0, 0)

    >>> year_of_season('12-2013', first=True)
    datetime.datetime(2012, 1, 1, 0, 0)

    >>> year_of_season('15')
    datetime.datetime(2015, 1, 1, 0, 0)

    >>> year_of_season('15', first=True)
    datetime.datetime(2015, 1, 1, 0, 0)
    
    >>> year_of_season('1999-00')
    datetime.datetime(2000, 1, 1, 0, 0)

    >>> year_of_season('1950-51')
    datetime.datetime(1951, 1, 1, 0, 0) 

    >>> year_of_season('1914-15')
    datetime.datetime(1915, 1, 1, 0, 0) 

    >>> year_of_season('14-1915', first=True)
    datetime.datetime(1914, 1, 1, 0, 0) 

    >>> year_of_season('2000-2013', first=True)
    Traceback (most recent call last):
        ...
    ValueError: invalid season string

    >>> year_of_season('rubbish')
    Traceback (most recent call last):
        ...
    ValueError: time data 'rubbish' does not match format '%Y'
    """

    try:
        top, bot = season.split('-')
    except ValueError:
        return strpyear(season)
    except AttributeError:
        return year_of_season(str(season))
    else:
        if first:
            return strpyear(top)
        else:
            return strpyear(bot)

def date_to_season_str(date):
    """
    >>> date_to_season_str(datetime.datetime(2013, 2, 4))
    '2012-13'

    >>> date_to_season_str(datetime.date(2013, 2, 4))
    '2012-13'

    >>> date_to_season_str(datetime.datetime(2006, 1, 1))
    '2005-06'

    >>> date_to_season_str(datetime.datetime(2013, 12, 6))
    '2013-14'
    """
    return '{0}-{1}'.format((date-YEAR_DELTA).strftime('%Y'), date.strftime('%y')) 

def current_season(offset=0):
    """
    >>> current_season() == date_to_season_str(datetime.datetime.now())
    True

    >>> current_season(offset=-4) == date_to_season_str(datetime.datetime.now()-4*YEAR_DELTA)
    True
    """
    offset_delta = relativedelta.relativedelta(years=offset)
    return date_to_season_str(datetime.datetime.now()+offset_delta)

def season_range(start, stop, step=1):
    """
    >>> season_range('2002', '2014') #doctest: +ELLIPSIS
    <generator object <genexpr> at 0x...>

    >>> list(season_range('2002', '2014')) #doctest: +NORMALIZE_WHITESPACE
    ['2001-02', '2002-03', '2003-04', '2004-05', 
    '2005-06', '2006-07', '2007-08', '2008-09', 
    '2009-10', '2010-11', '2011-12', '2012-13']

    >>> list(season_range(datetime.date(2002, 3, 5), \
            datetime.datetime(2014, 7, 12))) #doctest: +NORMALIZE_WHITESPACE
    ['2001-02', '2002-03', '2003-04', '2004-05', 
    '2005-06', '2006-07', '2007-08', '2008-09', 
    '2009-10', '2010-11', '2011-12', '2012-13']

    >>> list(season_range('2014', '2002'))
    []

    >>> list(season_range('2002', '2009', -2))
    []

    >>> list(season_range('2002-03', '2014')) #doctest: +NORMALIZE_WHITESPACE
    ['2002-03', '2003-04', '2004-05', '2005-06', 
    '2006-07', '2007-08', '2008-09', '2009-10', 
    '2010-11', '2011-12', '2012-13']

    >>> list(season_range('2002-03', '2014', 4)) # Gotcha - leap year in between
    ['2002-03', '2006-07', '2010-11']

    >>> list(season_range('2014-15', '2000-01', -1)) #doctest: +NORMALIZE_WHITESPACE
    ['2014-15', '2013-14', '2012-13', '2011-12', 
    '2010-11', '2009-10', '2008-09', '2007-08', 
    '2006-07', '2005-06', '2004-05', '2003-04', 
    '2002-03', '2001-02', '2000-01']

    >>> list(season_range('2014-15', '1951', -5)) #doctest: +NORMALIZE_WHITESPACE
    ['2014-15', '2009-10', '2004-05', '1999-00', 
    '1994-95', '1989-90', '1984-85', '1979-80', 
    '1974-75', '1969-70', '1964-65', '1959-60', 
    '1954-55']
    """

    step_delta = step * YEAR_DELTA
    # step_delta = step * datetime.timedelta(days=365)

    if isinstance(start, datetime.datetime) or isinstance(start, datetime.date):
        start_date = year_of_season(start.year)
    else: 
        start_date = year_of_season(start)

    if isinstance(stop, datetime.datetime) or isinstance(start, datetime.date):
        stop_date = year_of_season(stop.year)
    else: 
        stop_date = year_of_season(stop)

    return (date_to_season_str(current) for current in \
        datetime_range(start_date, stop_date, step_delta))

def merge_dicts(*args):
    """
    Equivalent to::
        lambda *args: dict(chain(*map(lambda x: x.items(), args)))
    
    >>> a = {'x': 32, 'y': 12, 'z': 53}
    >>> b = {'u': 13, 'v': 10}
    >>> c = {'v': 88, 'w': 21, 'x': 98}
    
    >>> merge_dicts(a, b, c) == {'u': 13, 'w': 21, 'v': 88, 'y': 12, 'x': 98, 'z': 53}
    True

    >>> merge_dicts(a, b) == {'y': 12, 'x': 32, 'z': 53, 'u': 13, 'v': 10}
    ... # No overlap
    True

    >>> merge_dicts(b, c) == {'x': 98, 'u': 13, 'w': 21, 'v': 88}
    ... # Overlap
    True

    >>> merge_dicts(c, b) == {'x': 98, 'u': 13, 'w': 21, 'v': 10}
    ... # Overlap, different order gives different results
    True

    >>> merge_dicts(a) == a
    True

    >>> merge_dicts()
    {}
    """
    return dict(chain(*map(lambda x: x.items(), args)))

list_minus = lambda l, m: filter(lambda x: x not in m, l)
list_minus.__doc__ = """
>>> list_minus([1, 3, 4, 6], [1, 2, 4, 7, 9])
[3, 6]
>>> list_minus([1, 2, 4, 7, 9], [1, 3, 4, 6])
[2, 7, 9]
>>> list_minus([], [1, 2, 4, 7, 9])
[]
>>> list_minus([1, 3, 4, 6], [])
[1, 3, 4, 6]
>>> list_minus([], [])
[]
"""

def dict_subset(d, keys, proper=False, default=None):
    """
    Not to be confused with `fromkeys(seq[, value])`

    Roughly equivalent to::
        lambda d, keys: {key: d.get(key, default) for key in keys}

    >>> a = {'x': 32, 'y': 12, 'z': 53}
    >>> dict_subset(a, ['x', 'z']) == {'x': 32, 'z': 53}
    True
    >>> dict_subset({}, [])
    {}
    >>> dict_subset({}, ['x', 'z']) == {'x': None, 'z': None}
    True
    >>> dict_subset(a, [])
    {}
    >>> dict_subset(a, ['w', 'x', 'y']) == {'y': 12, 'x': 32, 'w': None}
    True
    >>> dict_subset(a, ['u', 'v']) == {'u': None, 'v': None}
    True
    >>> dict_subset(a, ['u', 'v'], default=4) == {'u': 4, 'v': 4}
    True

    >>> dict_subset(a, ['x', 'z'], proper=True) == {'x': 32, 'z': 53}
    True
    >>> dict_subset({}, [])
    {}
    >>> dict_subset({}, ['x', 'z'], proper=True)
    {}
    >>> dict_subset(a, [], proper=True)
    {}
    >>> dict_subset(a, ['w', 'x', 'y'], proper=True) == {'y': 12, 'x': 32}
    True
    >>> dict_subset(a, ['u', 'v'], proper=True)
    {}
    >>> dict_subset(a, ['u', 'v'], proper=True, default=4)
    ... # default is ignored if proper is True
    {}
    """
    if proper:
        return {key: d[key] for key in keys if key in d}
    else:
        return {key: d.get(key, default) for key in keys}

dict_minus = lambda d, *keys: _dict_minus(d, keys)

def _dict_minus(d, keys):
    """
    >>> a = {'x': 32, 'y': 12, 'z': 53}

    >>> _dict_minus(a, ['y']) == {'x': 32, 'z': 53}
    True

    >>> _dict_minus({}, [])
    {}

    >>> _dict_minus(a, []) == a
    True

    >>> _dict_minus({}, ['x', 'y'])
    {}

    >>> _dict_minus(a, a.keys())
    {}

    >>> _dict_minus(a, ['v', 'w', 'x']) == {'y': 12, 'z': 53}
    True

    >>> _dict_minus(a, ['u', 'v', 'w']) == a
    True
    """
    return {key: d[key] for key in d if key not in keys}

# TODO: come up with catchier names 

def iter_of_dicts_to_nested_dict(iterable, key=None):
    """
    Roughly equivalent to::
        lambda lst, key: {d[key]: d for d in lst}

    >>> l = [
    ...     {'id': 2, 'first_name': 'Malcolm', 'last_name': 'Reynolds'},
    ...     {'id': 3, 'first_name': 'Zoe', 'last_name': 'Washburne'},
    ...     {'id': 4, 'first_name': 'Jayne', 'last_name': 'Cobb'},
    ...     {'id': 5, 'first_name': 'Kaylee', 'last_name': 'Frye'},
    ...     {'id': 7, 'first_name': 'Wash', 'last_name': 'Washburne'},
    ... ]
    
    >>> iter_of_dicts_to_nested_dict(l, key='id') == {
    ...     2: {'first_name': 'Malcolm', 'last_name': 'Reynolds'}, 
    ...     3: {'first_name': 'Zoe', 'last_name': 'Washburne'}, 
    ...     4: {'first_name': 'Jayne', 'last_name': 'Cobb'}, 
    ...     5: {'first_name': 'Kaylee', 'last_name': 'Frye'}, 
    ...     7: {'first_name': 'Wash', 'last_name': 'Washburne'}
    ... }
    True

    >>> iter_of_dicts_to_nested_dict(l, key='last_name') == {
    ...     'Washburne': {'first_name': 'Wash', 'id': 7}, 
    ...     'Reynolds': {'first_name': 'Malcolm', 'id': 2}, 
    ...     'Frye': {'first_name': 'Kaylee', 'id': 5}, 
    ...     'Cobb': {'first_name': 'Jayne', 'id': 4}
    ... }
    True

    >>> iter_of_dicts_to_nested_dict([])
    {}

    >>> iter_of_dicts_to_nested_dict(l) == {
    ...     0: {'id': 2, 'first_name': 'Malcolm', 'last_name': 'Reynolds'},
    ...     1: {'id': 3, 'first_name': 'Zoe', 'last_name': 'Washburne'},
    ...     2: {'id': 4, 'first_name': 'Jayne', 'last_name': 'Cobb'},
    ...     3: {'id': 5, 'first_name': 'Kaylee', 'last_name': 'Frye'},
    ...     4: {'id': 7, 'first_name': 'Wash', 'last_name': 'Washburne'},
    ... }
    True

    >>> m = [
    ...     {'x': 32, 'y': 12, 'z': 53},
    ...     {'u': 13, 'v': 10},
    ...     {'v': 88, 'w': 21, 'x': 98}
    ... ]

    >>> iter_of_dicts_to_nested_dict(m, key='x')
    Traceback (most recent call last):
        ...
    KeyError: 'x'
    """
    if key is not None:
        return {d[key]: dict_minus(d, key) for d in iterable}
    else:
        return {i: d for i, d in enumerate(iterable)}

# deprecated
list_of_dicts_to_dict_of_dicts = lambda lst, key: {d[key]: d for d in lst}

def iter_of_list_to_iter_of_dicts(iterable, header):

    if not header and iterable:
        raise ValueError('empty header')
    
    return (dict(zip(header, row)) for row in iterable)

iter_of_list_to_list_of_dicts = lambda iterable, header: list(iter_of_list_to_iter_of_dicts(iterable, header))
iter_of_list_to_list_of_dicts.__doc__ = """
Roughly equivalent to::
    lambda iterable, header: dict(zip(header, row)) for row in iterable

>>> a = [
...     [2, 'Malcolm', 'Reynolds'],
...     [3, 'Zoe', 'Washburne'],
...     [4, 'Jayne', 'Cobb'],
...     [5, 'Kaylee', 'Frye'],
...     [7, 'Wash', 'Washburne'],
... ]

>>> iter_of_list_to_list_of_dicts(a, ['id', 'first_name', 'last_name']) == [
...     {'id': 2, 'first_name': 'Malcolm', 'last_name': 'Reynolds'},
...     {'id': 3, 'first_name': 'Zoe', 'last_name': 'Washburne'},
...     {'id': 4, 'first_name': 'Jayne', 'last_name': 'Cobb'},
...     {'id': 5, 'first_name': 'Kaylee', 'last_name': 'Frye'},
...     {'id': 7, 'first_name': 'Wash', 'last_name': 'Washburne'},
... ]
True

>>> iter_of_list_to_list_of_dicts(a, ['id', 'last_name']) == [
...    {'last_name': 'Malcolm', 'id': 2}, 
...    {'last_name': 'Zoe', 'id': 3}, 
...    {'last_name': 'Jayne', 'id': 4}, 
...    {'last_name': 'Kaylee', 'id': 5}, 
...    {'last_name': 'Wash', 'id': 7}
... ]
True

>>> iter_of_list_to_list_of_dicts([], [])
[]

>>> iter_of_list_to_list_of_dicts([], ['id', 'last_name'])
[]

>>> iter_of_list_to_list_of_dicts(a, [])
Traceback (most recent call last):
    ...
ValueError: empty header

>>> iter_of_list_to_list_of_dicts(a, ['id', 'first_name', 'last_name', 'birthdate']) == [
...     {'id': 2, 'first_name': 'Malcolm', 'last_name': 'Reynolds'},
...     {'id': 3, 'first_name': 'Zoe', 'last_name': 'Washburne'},
...     {'id': 4, 'first_name': 'Jayne', 'last_name': 'Cobb'},
...     {'id': 5, 'first_name': 'Kaylee', 'last_name': 'Frye'},
...     {'id': 7, 'first_name': 'Wash', 'last_name': 'Washburne'},
... ]
True

>>> b = [
...     [],
...     [2, 'Malcolm'],
...     [3, 'Zoe', 'Washburne', '11/12/1972'],
...     [4, 'Jayne', 'Cobb'],
...     [5, 'Kaylee', 'Frye', '03/11/1985', 'Mechanic'],
...     [7, 'Wash', 'Washburne'],
... ]

>>> iter_of_list_to_list_of_dicts(b, [])
Traceback (most recent call last):
    ...
ValueError: empty header

>>> iter_of_list_to_list_of_dicts(b, ['id', 'first_name', 'last_name']) == [
...     {},
...     {'id': 2, 'first_name': 'Malcolm'},
...     {'id': 3, 'first_name': 'Zoe', 'last_name': 'Washburne'},
...     {'id': 4, 'first_name': 'Jayne', 'last_name': 'Cobb'},
...     {'id': 5, 'first_name': 'Kaylee', 'last_name': 'Frye'},
...     {'id': 7, 'first_name': 'Wash', 'last_name': 'Washburne'},
... ]
True

>>> iter_of_list_to_list_of_dicts(b, ['id', 'last_name']) == [
...     {},
...     {'id': 2, 'last_name': 'Malcolm'},
...     {'id': 3, 'last_name': 'Zoe'},
...     {'id': 4, 'last_name': 'Jayne'},
...     {'id': 5, 'last_name': 'Kaylee'},
...     {'id': 7, 'last_name': 'Wash'},
... ]
True

>>> iter_of_list_to_list_of_dicts(b, ['id', 'first_name', 'last_name', 'birthdate']) == [
...     {},
...     {'id': 2, 'first_name': 'Malcolm'},
...     {'id': 3, 'first_name': 'Zoe', 'last_name': 'Washburne', 'birthdate': '11/12/1972'},
...     {'id': 4, 'first_name': 'Jayne', 'last_name': 'Cobb'},
...     {'id': 5, 'first_name': 'Kaylee', 'last_name': 'Frye', 'birthdate': '03/11/1985'},
...     {'id': 7, 'first_name': 'Wash', 'last_name': 'Washburne'},
... ]
True
"""

# deprecated
list_of_lists_to_iter_of_dicts = lambda lst, cols: (dict(zip(cols, row)) for row in lst)
# deprecated
list_of_lists_to_list_of_dicts = lambda lst, cols: list(list_of_lists_to_iter_of_dicts(lst, cols))

split_dict_to_iter_of_dicts = lambda d, iterable_key, header_key: \
    iter_of_list_to_iter_of_dicts(d[iterable_key], d[header_key])

split_dict_to_list_of_dicts = lambda d, iterable_key, header_key: \
    list(split_dict_to_iter_of_dicts(d, iterable_key, header_key))

split_dict_to_list_of_dicts.__doc__ = """
>>> a = {
...     'rows': [
...         [2, 'Malcolm', 'Reynolds'],
...         [3, 'Zoe', 'Washburne'],
...         [4, 'Jayne', 'Cobb'],
...         [5, 'Kaylee', 'Frye'],
...         [7, 'Wash', 'Washburne'],
...     ],
...     'header': ['id', 'first_name', 'last_name'],
...     'other': 'anything else'
... }

>>> split_dict_to_list_of_dicts(a, 'rows', 'header') == [
...     {'id': 2, 'first_name': 'Malcolm', 'last_name': 'Reynolds'},
...     {'id': 3, 'first_name': 'Zoe', 'last_name': 'Washburne'},
...     {'id': 4, 'first_name': 'Jayne', 'last_name': 'Cobb'},
...     {'id': 5, 'first_name': 'Kaylee', 'last_name': 'Frye'},
...     {'id': 7, 'first_name': 'Wash', 'last_name': 'Washburne'},
... ]
True

>>> split_dict_to_list_of_dicts(a, 'rowSet', 'header')
Traceback (most recent call last):
    ...
KeyError: 'rowSet'

>>> split_dict_to_list_of_dicts(a, 'rowSet', 'Headers')
Traceback (most recent call last):
    ...
KeyError: 'rowSet'

>>> split_dict_to_list_of_dicts(a, 'rows', 'Headers')
Traceback (most recent call last):
    ...
KeyError: 'Headers'
"""

if __name__ == "__main__":
    import doctest
    doctest.testmod()
