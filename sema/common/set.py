import os

def setting_value(path_to_dot_setting, setting_name, value):
    """Returns 200: Successful,
       701: Setting name was not found in .setting"""

    value = str(value).strip() #Input could be str or int so let's cover both

    file_r = open(path_to_dot_setting, 'r')
    file_temp = open(path_to_dot_setting + '.temp', 'w')

    success = False

    for line in file_r.readlines():
        if line[0] == ' ' or line[0] == '\n':
            pass
        elif setting_name.upper().strip() == line[:line.find(':')].upper().strip() and line[0] != '#':
            success = True
            file_temp.write(line[:line.find(':')] + ':' + value.strip() + '\n')
        else:
            file_temp.write(line)

    file_r.close()
    file_temp.close()

    os.remove(path_to_dot_setting)
    os.rename(path_to_dot_setting + '.temp', path_to_dot_setting)

    if success:
        return 200
    else:
        return 701


