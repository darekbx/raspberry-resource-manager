## Raspberry Pi Resource Manager Flask app

#### Project structure
* **run.py** - start point of the app, to start application just run `python3 run.py`
* **requirements.txt** - list of required python modules
* **app** - directory with the application
  * **templates** - directory with html templates
  * **\_\_init\_\_.py** - here is the application initialized
  * **configuration.py** - configuration reader (configuration is stored in configuration.json file)
  * **models.py** - file with database models (tables)
  * **views.py** - file contains routes with views, like "/" or "/login" 
  * **resource-manager.db** - sqlite database file

#### Installation
Enter to project directory and add dir:<br/>
`mkdir venv`<br/>

Then run:<br/>
`python3 -m venv venv`<br/>

Install Python PIP (OS X):<br/>
`sudo easy_install pip`<br/>

Install Flask:<br/>
`python3 -m pip install Flask`<br/>

Install Flask-SQLAlchemy:<br/>
`python3 -m pip install Flask-SQLAlchemy`<br/>
