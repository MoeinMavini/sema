import os
import lxml.etree as ET

def create_setting_file(path):
    if os.path.isfile(path):
        return 701

    if os.path.isfile(path + '.setting.xml'):
        return 702

    try:
        root = ET.Element("root")
        
        tree = ET.ElementTree(root)
        tree.write(path + '.setting.xml', xml_declaration=True, pretty_print=True)

        file = open(path, 'w')

        file.close()

        return 200

    except Exception as e:

        try:
            os.remove(path + '.setting.xml')
        except OSError:
            pass

        try:
            os.remove(path)
        except OSError:
            pass

        return e

def edit(path):
    print('Edit')





