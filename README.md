# sema
sema is a setting maker that lets user change the setting safely and with lots of information about what can be done.  

# What is sema
I have faced many setting files that all the available options for a setting or meaning of changes are hard to find
or the only way to understand the options is through indirect sites. the other issue is the certainty that
am i doing the changes the right way or will i break the system with the wrong syntax? In essence settings are painful to
deal with, but i am tring to make it easier through giving user a program to alter settings with and shippng informations
about settings with the setting it self in a seprate file, so user has some suggestions and informations about what can be
done.  
## Future of sema
This is just a beta version, there are futures that are not done yet like: support for multivalues for an
option and much more, and there are bugs and also possibility of revisions.  

So basiclly there is much to be done, at this phase i just want people to see the idea and give feedbacks to me, i would 
love to hear about ideas and know why you like or hate this idea. Feel free to ask or say anything.  

# Installation
Use `pip install sema` to install `sema` 
or download sema repository from github and open terminal in root of the project then type `python setup.py build`
 after that type `python setup.py install`  
## For creating and managing settings for developers
`sema` and `sema -cli` are available in terminal for creating and managing settings for developers.
## Reading settings in your program
To extract settings in your program use `from sema import extract`, for now there is only 1 function in the library which
returns the value for given option name `get_value(file_name, option_name)`
## Altering the settings for users
Use change_setting_gui.py and change_setting_cli.py files in change_setting folder to alter settings.  
To give the addresses of .setting file(s) you want this script to be responsible for, there are 2 ways:  
	1. Enter the addresses in sema_files file line by line, in the same folder as the script  
	2. Enter them in `dot_setting_list` inside the script   