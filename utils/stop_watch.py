import time
from datetime import datetime


def start_dt() -> datetime:
    """Show the start time.
    
    Returns
    -------
    datetime
        The date time this call was made.
    """
    dt = datetime.now()
    print('stop_watch', 'Started>', dt.isoformat(timespec='microseconds'), flush=True)
    return dt


def elapsed_dt(start_datetime: datetime = datetime.now(), text: str = 'Elapsed>') -> datetime:
    """Show the delta time.
    
    Parameters
    ----------
    start_datetime: datetime, option, default now 
        The time you want to subtract from the current time.
    text: str, optional 
        The text to appear in the print statement. 
        
    Returns
    -------
    datetime
        The date time this call was made.
    """
    dt = datetime.now()
    print('stop_watch', text,
          dt.isoformat(timespec='microseconds'), '\t',
          start_datetime.isoformat(timespec='microseconds'),
          '\t Diff: ', dt - start_datetime,
          flush=True)
    return dt


if __name__ == '__main__':
    help(start_dt)
    help(elapsed_dt)

    elapsed_dt(text='Sample>')
    my_dt = start_dt()
    time.sleep(1)
    my_dt = elapsed_dt(my_dt)
    time.sleep(2)
    my_dt = elapsed_dt(my_dt)
