# BookJo RestAPI

> [!CAUTION]
> Based on the `.env.example` in the `config/env` directory, first set the `.env` file in the same folder

## Usage

Project is accessible on the 8000 port

### **Docker:**

To use docker just run `sudo docker compose up --build -d`. it will create images and hence you can have access to the project

### **Local:**

To run the porject localy without docker:

> - **First:** navigate to `src` directory
>
> - **Second:** activate the environment(if you are using pip, install the dependecies with whatever command it is, a requirements.txt file is provided. but if you are using UV (which is awesome) just type uv sync and done!) by using `source .venv/bin/activate`(*I dont know the windows usecase)
>
> - **Third:** `python manage.py makemigrations`, `python manage.py migrate` and `python manage.py runserver`
_

> [!IMPORTANT]
> **To see the celery beat tasks if you are using the docker you should tail the logs of the celery and celery-beat services, but if you are tryin to run the project locally you should use this commands to run the celery and beat in separate terminals with pwd of src**
>
> - `celery -A config beat -l INFO`
> - `celery -A config worker -l INFO`

## Architecture

I did it as simple and efficient as possible, although i'm aware that ther might be some flaws in implementation; but i think its clean to read and open to updates

- **`src/`**: is where the whole magic happens
  - **`apps/`**: contains two apps;
  - - `core` wihch is reponsible for _authentication_
  - - `library` which containts most of the projces' _logic_
  - **`common/`**: contains the necessary `common helper tools` for project including: _responses_, _mixins_, _exceptions_, _models_ and _permissions_
  - **`config/`**: settings, env, urls, celery and wsgi servers are in it, settings were supposed to inlcude multiple settings for the production and development environments but its a premeature architecural design pattern for now. env contains an .env.example which is an example for the keys you should set to run the project in the .env file in the same directory

> [!NOTE]
>Development DB is SQLite3 for obvious reasons, but the production is PostgreSQL
>
>I used the repo/service pattern, although again this might not be necessary at this level but i prefer a clean separation of concerns for all my projects
>
>Also, still an logger need to be configured for nay project but this one is an exception =]

## Information

> [!TIP]
>
>- To set the due date for the book set the `DUE_DATE_PERIOD_DAY` key in the .env file
>- `CELERY_BEAT_SCHEDULE` in the **settings.base** is where the beat tasks are, to change them period, change the schedule keys' value
>- _swagger_ doc is accessible from the `api/docs` url
