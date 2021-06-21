#This is not a useful program but it shows the use of settings
from sema import extract

char1 = char2 = '*'
is_ascending = 'true'
asd_dsc_lenght = 12
asd_dsc_position = 'rtl'
rectangle_lenght = 15
rectangle_width = 8

temp = extract.get_value('asd-dsc.setting', 'Char')
if 'Value' in temp:#It has value
    char1 = temp['Value']
else:
    print('char1: ' + temp['message'])#Prints the error

temp = extract.get_value('rectangle.setting', 'Char')
if 'Value' in temp:
    char2 = temp['Value']
else:
    print('char2: ' + temp['message'])

temp = extract.get_value('asd-dsc.setting', 'ascending')
if 'Value' in temp:
    is_ascending = temp['Value']
else:
    print('is_ascending: ' + temp['message'])

temp = extract.get_value('asd-dsc.setting', 'lenght')
if 'Value' in temp:
    asd_dsc_lenght = temp['Value']
else:
    print('asd_dsc_lenght: ' + temp['message'])

temp = extract.get_value('asd-dsc.setting', 'position')
if 'Value' in temp:
    asd_dsc_position = temp['Value']
else:
    print('asd_dsc_position: ' + temp['message'])

temp = extract.get_value('rectangle.setting', 'lenght')
if 'Value' in temp:
    rectangle_lenght = temp['Value']
else:
    print('rectangle_lenght: ' + temp['message'])

temp = extract.get_value('rectangle.setting', 'width')
if 'Value' in temp:
    rectangle_width = temp['Value']
else:
    print('rectangle_width: ' + temp['message'])


print('asd-dsc char: ' + char1 + ', rectangle char: ' + char2 + ', shape 1 is ', end = '')

print('ascending,' if is_ascending == 'true' else 'dscending,')

print('shape 1 has max lenght of ' + asd_dsc_lenght + ', it forms from ' + asd_dsc_position +
     ',\nrectangle has the lenght and width of ' + rectangle_lenght + ', ' + rectangle_width + '.')

input()
#TODO Make shape A and B

