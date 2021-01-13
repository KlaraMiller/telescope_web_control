# Telescope Web Control

Code written for a bachelor thesis to control a telescope with a web control designed with Django Channels.

### Program Crash Warning
Program crashes when one of the following celestial objects are selected in ‘Observe Object’: Moon, ISS, planets and star ‘Boteln’. This is part of the implementation of previous bachelor thesis’ and fixing this issue was not part of this bachelor thesis.

### Explanation ‘temp’ folder
The project consists of two folders ‘src’ and ‘tmp’. ‘src’ consists of the developed code for this project. ‘tmp’ consists of a lot of files, which some of them are needed for certain packages, but doesn’t contain program code.

### Folder names on zybo board
Project folder: /home/debian/miller/webcontrol/venv/src

Virtual Environment (venv) folder: /home/debian/miller/webcontrol/venv

Activate venv: $ source /home/debian/miller/webcontrol/venv/bin/activate

### Starting server
Server does not start automatically. To start server for the website to be online run following three scripts: manage.py, motor_control_and_observe.py, sensor_data.py (Further resources: ‘PyCharm Project Setup.pdf)

#### Known issue
Starting the server from the command line fails do to Python package management problems. Set up a PyCharm project as described in the guide and run the server with the run configuration. 

### Database
Database can be cleared with script ‘reset_database.py’

### Python Version for project
Python 3.7
