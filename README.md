# Movies list app
This project provides a page with list of films from Studio Ghibli

## Project Requirements
Any commands listed below are assuming to be run from project root directory at your terminal
To run the project you need the following to be installed on your machine:
- Python 3.7
- Memcached

### VirtualEnv
To create a virtual environment with `virtualenv` and install required packages run the following:

```
$ virtualenv -p python3.7 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Environment Variables
Before project run you need to provide the following environment variables:
```
$ export DJANGO_SETTINGS_MODULE=movie_list.settings
$ export SECRET_KEY=<hash>
```

### Migration
Before project run you need to apply migrations
```
$ python manage.py migrate
```

### Run Memcached
Open up your terminal and run:
```
$ memcached
```
This command will run Memcached in attached mode. To run it in detached (daemon) mode, run:
```
$ memcached -d
```

### Run project
By default the project runs on the port 8000. [URL](http://127.0.0.1:8000/movies/)
```
$ python manage.py runserver
```

### Testing
Run the following command to run tests:
```
python manage.py test
```

### Code style check
Flake8 is used for code style check. Run the following command to perform code style check:
```
./run_flake8.sh
```
With successfully passed check you'll see the following message:  
```
Flake8 verification has passed!
```
.. otherwise issues will be displayed 
