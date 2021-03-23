"""This module directs the 'sema' command line to gui or cli"""
import sys

def main():
    arg1 = ''

    if len(sys.argv) > 1:
        arg1 = sys.argv[1]

    if arg1.lower() == '-cli':
        from sema.manage_setting import manage_setting_cli
        manage_setting_cli.start()
    else:
        from sema.manage_setting import manage_setting_gui
        manage_setting_gui.start()

if __name__ == "__main__":
    main()

