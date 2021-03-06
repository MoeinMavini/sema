"""This library is used to extract data from a setting maker file in code
it has only one function: get_value to get value of an option"""
from sema.common import check

def get_value(file_name, option_name):
    """This function is used to get the value of an option in the specified file
    File name can include path
    
    returns:
        {'Error':700, 'message':message} == .setting file not found! this file holds the values
        {'Error':701, 'message':message} == option name not found
        {'Value':value} == Returns options value"""

    verfy_result = check.file_exists(file_name, False)

    if verfy_result == 701:
        return {'Error':700, 'message': 'File ' + file_name + ' is not valid'}
    else:
        file = open(verfy_result, 'r')

        for line in file.readlines():
            if line[0] == '#' or line[0] == ' ' or line[0] == '\n':
                pass
            elif option_name.upper().strip() == line[:line.find(':')].upper().strip():
                file.close()
                return {'Value':line[line.find(':')+1:].strip()}

        file.close()
        return {'Error':701, 'message': 'Option name not found'}

