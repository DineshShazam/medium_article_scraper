import requests
import logging as log
import sys


log.basicConfig(level=log.INFO,format='%(levelname)s:%(message)s')


#! try catch decorator
def exception_handler(func):
    def wrapper_func(*args,**kwargs):
        try:
            return func(*args,*kwargs)
        except requests.exceptions.RequestException as e:
            log.error(f'{func.__name__} API request failed to execute. {e}')
            sys.exit()
        except FileNotFoundError as e:
            log.error(f'{func.__name__} File failed to execute. {e}')
            sys.exit()
        except ValueError:
            log.error(f'{func.__name__} Invalid value format.')
            sys.exit()
        except Exception as e:
            log.error(f'{func.__name__} failed to execute. {e}')
            sys.exit()
    
    return wrapper_func

# get the month and date of the specified no of days
@exception_handler
def get_day_month(no_of_days : int) -> tuple[int, int]:
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    m = 0
    d = 0
    while no_of_days > 0:
        d = no_of_days
        no_of_days -= month_days[m]
        m += 1

    return (m,d)

@exception_handler
def get_claps_count(claps_string : str) -> int :
    if (claps_string == '') or (claps_string is None) or (claps_string.split is None):
        return 0
    claps_split = claps_string.split('K')
    no_of_claps = float(claps_split[0])
    no_of_claps = int(no_of_claps*1000) if len(claps_split) == 2 else int(no_of_claps)
    return no_of_claps