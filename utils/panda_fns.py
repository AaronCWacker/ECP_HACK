import pandas as pdb


def get_col_as_str(row: pdb.DataFrame, col_name: str, default_value: str= '', throw_err: bool=False) -> str:
    """Get the str value out of the specified column
    
        :param row: row to get a value out of
        :param col_name: name of the column 
        :param default_value: expected return value on error 
        :param throw_err: default False, otherwise throw an error.  Useful for development.
        :return: the str value in the specified column 
    """
    try:
        return str(row[col_name]).strip()
    except Exception as err:
        if throw_err:
            raise err
        return default_value


def get_col_as_int(row: pdb.DataFrame, col_name: str, default_value: int=0, throw_err: bool=False) -> int:
    """Get the int value out of the specified column.
      
        :param row: row to get a value out of
        :param col_name: name of the column 
        :param default_value: expected return value on error
        :param throw_err: default False, otherwise throw an error.  Useful for development.
        :return: the int value in the specified column 
    """
    try:
        return int(row[col_name])
    except Exception as err:
        if throw_err:
            raise err
        return default_value
