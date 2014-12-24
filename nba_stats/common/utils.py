import datetime
from dateutil import relativedelta
from itertools import chain

# TODO: Unit/regression testing
# TODO: Documentation

YEAR = relativedelta.relativedelta(years=1)

def time_range(start, stop, step):
    current = start
    if step.days < 0:
        while current >= stop:
            yield current
            current += step
    else:
        while current < stop:
            yield current
            current += step

def year_of_season(season_str, first=False):
    try:
        top, bot = season_str.split('-')
    except ValueError:
        return datetime.datetime.strptime(season_str, '%Y')
    else:
        if first:
            return datetime.datetime.strptime(top, '%Y')
        else:
            return datetime.datetime.strptime(bot, '%y')

def date_to_season_str(date):
    return '{0}-{1}'.format((date-YEAR).strftime('%Y'), date.strftime('%y')) 

def current_season(offset=0):
    offset_delta = relativedelta.relativedelta(years=offset)
    return date_to_season_str(datetime.datetime.now()+offset_delta)

def season_range(start, stop, step=1):
    step_delta = relativedelta.relativedelta(years=step)
    
    if isinstance(start, datetime.datetime):
        start_date = start
    else: 
        start_date = year_of_season(start)

    if isinstance(stop, datetime.datetime):
        stop_date = stop
    else: 
        stop_date = year_of_season(stop)

    return (date_to_season_str(current) for current in \
        time_range(start_date, stop_date, step_delta))

merge_dicts = lambda *args: dict(chain(*map(lambda x: x.items(), args)))

# TODO: come up with catchier names 
list_of_dicts_to_dict_of_dicts = lambda lst, key: {d.pop(key): d for d in lst}
list_of_lists_to_iter_of_dicts = lambda lst, cols: (dict(zip(cols, row)) for row in lst)
list_of_lists_to_list_of_dicts = lambda lst, cols: list(list_of_lists_to_iter_of_dicts(lst, cols))
split_dict_to_iter_of_dicts = lambda d, lst_key, col_key: list_of_lists_to_iter_of_dicts(d[lst_key], d[col_key])
split_dict_to_list_of_dicts = lambda d, lst_key, col_key: list_of_lists_to_list_of_dicts(d[lst_key], d[col_key])
