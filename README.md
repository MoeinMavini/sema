# sema
sema is a setting maker that lets user change the setting safely and with lots of information about what can be done.

**Prototype version!**

# What is sema
I have faced many setting files that, all the available options for a setting or what does changes mean, are hard to find
or the only way to understand most of options is through indirect sites, the other issue is the certainty that
am i doing the changes the right way and will i break the system with wrong syntax. In essence settings are painful to
deal with, but i am tring to make it easier through giving user a program to alter settings with and shippng informations
about settings with the setting it self in a seprate file, so user has some suggestions and informations about what can be
done.
## Future of sema
This is just a prototype, there are futures that are not done yet like: Tkinter version and support for multivalue for a 
setting and much more, and there are bugs and also possibility of revisions.

So basiclly there is much to be done, at this phase i just want people to see the idea and give feedbacks to me, i would 
love to hear about ideas and know why you like or hate this idea. Feel free to ask or say anything.

# Installation
## For creating and managing settings for developers
Use `pip install sema` to install `sema` for command line and sema library
Or download the project and open the terminal in root of the project and type `python setup.py build` then type 
`python setup.py install`
Command line version is for creating and managing settings for developers and library is for reading settings in your 
program.
To start sema in command line type `sema`.
## Reading settings in your program
Use `pip install sema` to install `sema` for command line and sema library
Or download the project and open the terminal in root of the project and type `python setup.py build` then type 
`python setup.py install`
Command line version is for creating and managing settings for developers and library is for reading settings in your 
program.
To use `sema` in your program use `import sema`, now there is only 1 function in library which return the value for
the given setting name.
## Altering the settings for users
Use change_setting.py file in change_setting folder to alter settings.
To give the address of .setting file(s) you want this script to be responsible of there are 2 ways:
	1. Enter the addresses in sema_files file line by line, in the same folder as the script
	2. Enter them in `dot_setting_list` inside the script 