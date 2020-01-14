# page-analyzer
### Local Development
#### Prerequisites
- Docker ([Docker installation guide](https://docs.docker.com/install/#supported-platforms));
- Docker Compose ([Docker Compose installation guide](https://docs.docker.com/compose/install/)).
- pre-commit ([pre-commit installation document](https://pre-commit.com/#install)).

#### Install pre-commit hooks
Install `pre-commit` into your git hooks:
```bash
$ pre-commit install
```
You can read more about `pre-commit` usage: https://pre-commit.com/#usage 

#### Configuring the Environment
You can find all environment variables under ```docker/``` directory. This is how it looks like:
```bash
docker
├── app
│   ...
│   └── .env
└── db
    ...
    └── .env
```
If there are no environment files you can copy it manually from ```env.examples``` directory:
```bash
$ cp envs.example/app.env docker/app/.env
$ mkdir docker/db/ && cp envs.example/db.env docker/db/.env
```

#### Build the Stack
This can take a while, especially the first time you run this particular command on your development system
```bash
$ docker-compose -f local.yml build
```

#### Run the Stack
This brings up all services together. The first time it is run it might take a while to get started, but subsequent runs will occur quickly.

Open a terminal at the project root and run the following for local development
```bash
$ docker-compose -f local.yml up -d
```
This command starts the containers in the background and leaves them running.

In case you want to aggregate the output of each container use following command
```bash
$ docker-compose -f local.yml up
```

You can also set the environment variable ``COMPOSE_FILE`` pointing to ``local.yml`` like this
```bash
$ export COMPOSE_FILE=local.yml
```

And then run
```bash
$ docker-compose up -d
```

#### Create a superuser
```bash
$ docker-compose -f local.yml exec app python manage.py createsuperuser
```

#### Populate database
Load *flatpages* and *support center initial* data
```bash
$ docker-compose -f local.yml exec app python manage.py loaddata flatpages supportcenter
```

#### Generate thumbnails
Anytime you change size of thumbnails you need to regenerate cache of those
```bash
$ docker-compose -f local.yml exec app python manage.py generateimages
```

#### Stop the Stack
To stop, just
```bash
$ docker-compose -f local.yml stop
```

#### Start the Stack
To start the stack in case containers are existing use this command
```bash
$ docker-compose -f local.yml start
```

#### Destroy the Stack
To stop containers and remove containers and networks
```bash
$ docker-compose -f local.yml down
```
To stop containers and remove containers, networks and local images
```bash
$ docker-compose -f local.yml down --rmi local
```  
To stop containers and remove containers, networks, local images and volumes:
```bash
$ docker-compose -f local.yml down --rmi local -v
```
More information: https://docs.docker.com/compose/reference/down/

### Project services
| Service Name | Port |
| -------- | -------- |
| `app`   | `8000/tcp`   |
| `db`  | `5432/tcp`   |
| `redis`  | `6379/tcp`   |
| `celery`  |  |
| `celery_beat`  |  |

### Show logs in realtime
All logs  from all containers
```bash
$ docker-compose -f local.yml logs -f
```
Or you can watch logs from one service (container) - set service name
```bash
$ docker-compose -f local.yml logs -f service_name
```
Also you can trim logs command output
```bash
$ docker-compose -f local.yml logs -f --tail=20 service_name
```

#### SQL Formatter
To enable SQL command output in logs add this variables into `docker/app/.env` file 
```bash
DJANGO_DEBUG_SQL=on
DJANGO_DEBUG_SQL_COLOR=on
```
To change formatter style use `DJANGO_DEBUG_SQL_FORMATTER_STYLE` variable
```bash
DJANGO_DEBUG_SQL_FORMATTER_STYLE=solarized-light
```
To get all available styles, please [check documentation](http://pygments.org/docs/styles/#getting-a-list-of-available-styles).

### Testing and coverage
#### Tests
This project uses the [Pytest](https://docs.pytest.org/en/latest/index.html), a framework for easily building simple and scalable tests.

To perform testing just run the following command
```bash
$ docker-compose -f local.yml run --rm app pytest
```
To run `pytest` in verbose mode you can use `-v` option
```bash
$ docker-compose -f local.yml run --rm app pytest -v
```
##### Speed up test runs by sending tests to multiple CPUs
To send tests to multiple CPUs, use `-n` option
```bash
$ docker-compose -f local.yml run --rm app pytest -n 3
```
Especially for longer running tests or tests requiring a lot of I/O this can lead to considerable speed ups. This option can also be set to `auto` for automatic detection of the number of CPUs
([more information](https://github.com/pytest-dev/pytest-xdist#speed-up-test-runs-by-sending-tests-to-multiple-cpus)).
#### Coverage
You can run the ```pytest``` with code ```coverage``` by typing in the following command:
```bash
$ docker-compose -f local.yml run --rm app pytest --cov
```
After that you will see coverage report just below tests results. Also you can get access to HTML version of the report on [pages](https://page_analyzer.git.steelkiwi.com/backend/)

To show coverage report with missing terms just use command:
```bash
docker-compose -f local.yml run --rm app pytest --cov --cov-report term-missing
```
### Debugging 
If you are using the following within your code to debug:
```python
import ipdb; ipdb.set_trace()
```
Then you may need to run the following for it to work as desired:
```bash
$ docker-compose -f local.yml run --rm --service-ports app
```
#### Django Debug Toolbar
To enable Django Debug Toolbar just enable it in the `docker/app/.env` file
```bash
DJANGO_USE_DEBUG_TOOLBAR=on
```
### Execute Management Commands
As with any shell command that you wish to run in the container, this is done using the ```docker-compose -f local.yml exec``` command:
```bash
$ docker-compose -f local.yml exec app python manage.py migrate
$ docker-compose -f local.yml exec app python manage.py dbshell
```
In case you want to execute command in a temporary created docker container, use ```docker-compose -f local.yml run --rm``` command:
```bash
$ docker-compose -f local.yml run --rm app python manage.py migrate
$ docker-compose -f local.yml run --rm app python manage.py dbshell
```

### Create new app
To create new app inside current Django project you should do following commands:

Create the `app_name` app with `python manage.py startapp`
```bash
$ docker-compose -f local.yml exec app python manage.py startapp app_name
``` 
Manually move `app_name` folder to `page_analyzer/apps/`
```bash
$ mv app_name page_analyzer/apps/
```
Add `app_name.apps.AppNameConfigClass`, on `LOCAL_APPS` on `config/settings.py`

### Install new requirements
To add and install new requirements to the project you should add requirement into certain `requirements.txt` file like this:
```text
djangorestframework==3.9  # https://github.com/encode/django-rest-framework
```
and rebuild the container or whole stack
```bash
$ docker-compose -f local.yml up -d --build app
```

### Useful Docker commands
Show containers status
```bash
$ docker-compose -f local.yml ps
```
Manually restart a container
```bash
$ docker-compose -f local.yml restart service_name
```
Manually restart container and follow log output
```bash
docker-compose -f local.yml restart service_name && docker-compose -f local.yml logs -f --tail=20 service_name
```
Manually rebuild container and restart service
```bash
$ docker-compose -f local.yml up -d --build --no-deps service_name
```
Show containers performance
```bash
$ docker stats
```
Show volumes list
```bash
$ docker volume ls
```
Manually remove volume
```bash
$ docker volume rm volume_name
```
