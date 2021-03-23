def get_multiline_input(prompt):
    
    print(prompt + '\n***To end input, write nothing just press Enter (New line)***\n')

    content = ''

    while True:
        temp = input(':')

        if temp == '':
            break
        else:
            content += temp + '\n'
    
    return content[:-1]


