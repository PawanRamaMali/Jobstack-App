## FastAPI Connecting to a Database

 I would suggest you to try out Postgres as it is a production-grade db.
 We can use SQLite, It is a file system based, easy-to-use database and is supported by python.
 
 We will be using an ORM called sqlalchemy, ORM is a mapper which helps translate our database table records to a class object. To understand the benefit of it, I will actually tell, what happens if we don't use ORM. Most of the time, I have the responsibility of backend development in Django but sometimes I am given the responsibility of assignment verification for hiring. There was one student say 'John wick', he had made a wonderful UI and the assignment was working all fine but as a backend developer, I wanted to test his backend logic and test some corner cases, I started to install his project but there was a problem. He had used raw MySQL, and my machine did not have MySQL installed. In case he had used an ORM e.g. Django ORM, the ORM would handle the responsibility of translating DB queries to different databases. Thats why I am stressing for an ORM.

Ok let's add the following lines in requirements.txt: and run pip install -r requirements.txt


```
fastapi
uvicorn

#for template
jinja2

#for static files
aiofiles

#for database   #new
sqlalchemy         
psycopg2

#for loading environment variables  #new
python-dotenv
```

Now, what we want is to have information of the database but I won't suggest storing this information in raw form. Instead, I would suggest keeping this information in environment variables. To make this process of creating environment variables super easy we are going to make use of python-dotenv.  Let's create these new files #Todo:

In the '.env' file we are going to store critical information for our applications like api-keys, api-secret-key, database URL. So, lets put this info. in the '.env' file.

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=yourdbname_eg_debug
```

Now, I am going to modify our config file, this is because we don't want to directly communicate with '.env' file and instead we want to arrange all our project configurations at one specific place. In our case, it is config.py file. So, let's modify the config.py file to read from '.env; file and keep our configurations ready.


```py
import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME:str = "Job Board"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER","localhost")
    POSTGRES_PORT : str = os.getenv("POSTGRES_PORT",5432) # default postgres port is 5432
    POSTGRES_DB : str = os.getenv("POSTGRES_DB","tdd")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

settings = Settings()
```

Almost there, just stick with me for some time. This I am doing to make our project more maintainable. What I have learnt in my little experience is "Software development is more about maintenance and less about development".
Ok, now we can move to database setup, type the following lines in db > session.py

```py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#if you don't want to install postgres or any database, use sqlite, a file system based database, 
# uncomment below lines if you would like to use sqlite and comment above 2 lines of SQLALCHEMY_DATABASE_URL AND engine

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
```

* We are creating a sqlalchemy engine with postgres database URL. As stated earlier, you can create an engine with sqllite too. just uncomment the commented lines and comment out SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL 
engine = create_engine(SQLALCHEMY_DATABASE_URL)
* Then, we are creating a SessionLocal. Once we create an instance of the SessionLocal class, this instance will be the actual database session. Remember this thing, we will create an actual database session for each request later.

A model class is the pythonic representation of a database table. Alright, now we are going to create a super grandfather class. Every model will inherit this 'Base' class and we will utilize this base class to create all the database tables. Also, we will keep all common logic related to tables in this 'Base' class. For instance, all our table tables will have an id field. This will be used to uniquely identify each row/record. Lets create this Base class in a file db > base_class.py

```
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    #to generate tablename from classname
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
       
```

That was a lot, but there is one big thing missing. Think think 😁
Our app is in main.py file and It has no idea of whatever we are typing in other files! So, we have to tell our app to create our database tables for us. So, add the following code in main.py

```py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.config import settings
from apis.general_pages.route_homepage import general_pages_router
from db.session import engine   #new
from db.base_class import Base  #new


def include_router(app):
	app.include_router(general_pages_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables():           #new
	Base.metadata.create_all(bind=engine)

	
def start_application():
	app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
	include_router(app)
	configure_static(app)
	create_tables()       #new
	return app

app = start_application()

```
Now, If you are using postgres, open up PgAdmin and create a new database, same as that of mentioned by you in '.env' file. (yourdbname_eg_debug) and just restart the server. Our database and server are now connected to each other. In case we are using SQLite, we don't even need to create database manually. Just restart the server. Here is a gif of my postgres db connection

