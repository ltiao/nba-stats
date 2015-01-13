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
from itertools import chain

# TODO: Unit/regression testing
# TODO: Documentation

YEAR_DELTA = relativedelta.relativedelta(years=1)

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

merge_dicts = lambda *args: dict(chain(*map(lambda x: x.items(), args)))

# TODO: come up with catchier names 
list_of_dicts_to_dict_of_dicts = lambda lst, key: {d.pop(key): d for d in lst}
list_of_lists_to_iter_of_dicts = lambda lst, cols: (dict(zip(cols, row)) for row in lst)
list_of_lists_to_list_of_dicts = lambda lst, cols: list(list_of_lists_to_iter_of_dicts(lst, cols))
split_dict_to_iter_of_dicts = lambda d, lst_key, col_key: list_of_lists_to_iter_of_dicts(d[lst_key], d[col_key])
split_dict_to_list_of_dicts = lambda d, lst_key, col_key: list_of_lists_to_list_of_dicts(d[lst_key], d[col_key])

if __name__ == "__main__":
    import doctest
    doctest.testmod()