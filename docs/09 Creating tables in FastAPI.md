## Creating tables in FastAPI

 A request-response cycle basically means to understand what happens in between, the browser makes a request and FastAPI sends backs a response.
 
 ![image](https://user-images.githubusercontent.com/11299574/132248435-b419250a-4c03-42e5-8d78-309479c21603.png)

So, let's begin to create database tables. Make sure you have this folder structure. Create the models to hold the class equivalent of DB tables.

```
backend/
├─.env
├─apis/
│ └─general_pages/
│   └─route_homepage.py
├─core/
│ └─config.py
├─db/
│ ├─base.py
│ ├─base_class.py
│ ├─models/          #new folder
│ │ ├─jobs.py        #new file
│ │ └─users.py       #new file
│ └─session.py
├─main.py
├─requirements.txt
├─static/
│ └─images/
│   └─logo.png
└─templates/
  ├─components/
  │ └─navbar.html
  ├─general_pages/
  │ └─homepage.html
  └─shared/
    └─base.html

```

Type in the following code in db > models > jobs.py

```py
from sqlalchemy import Column, Integer, String, Boolean,Date, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Job(Base):
    id = Column(Integer,primary_key = True, index=True)
    title = Column(String,nullable= False)
    company = Column(String,nullable=False)
    company_url = Column(String)
    location = Column(String,nullable = False)
    description = Column(String,nullable=False)
    date_posted = Column(Date)
    is_active = Column(Boolean(),default=True)
    owner_id =  Column(Integer,ForeignKey("user.id"))
    owner = relationship("User",back_populates="jobs")

```

Ok, now let's understand what we just did and why:

* Remember in the last post I told you a story that it's we use raw SQL queries like "Select * from Job". It will not work with all the databases. Because each database has a different set of protocols/rules. e.g. in Postgres " double quotes are not recognized and we have to use ' single quotes.
* We have our Base class in 'base_class.py' and we are inheriting it to have a class-based representation of tables. Each property or attribute of this class is translated into a column in the table.
* The 'title' column represents Job title and it can store strings. Its value in the table can't be NULL.
* is_active columns will be used to control if the job post will be visible on the website or not. e.g. Job posts expire in few days so we can make a logic to toggle is_active to False in 2 weeks.
* The job table will have a foreign key to the User table and these foreign keys will be used to identify who is the job poster. This will be used to authorize if a person can update/delete a job post or not.


Now, we will also type in the code to have a User table which will be used to hold users data obviously. Type in the below code in db > models > users.py.

```py
from sqlalchemy import Column,Integer, String,Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class User(Base):
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,nullable=False)
    email = Column(String,nullable=False,unique=True,index=True)
    hashed_password = Column(String,nullable=False)
    is_active = Column(Boolean(),default=True)
    is_superuser = Column(Boolean(),default=False)
    jobs = relationship("Job",back_populates="owner")
    
 ```
 
 Lets put the import of all these models in one single file named 'base.py'. It will be helpful to create all the tables at once in our web app.
 
 
 ```py
 #db > base.py
from db.base_class import Base
from db.models.jobs import Job 
from db.models.users import User
```
Remeber we were importing 'Base' in main.py file and creating db tables. Now we won't import Base from base_class.py but instead from base.py. So, change the import statement in main.py to:

```py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.config import settings
from apis.general_pages.route_homepage import general_pages_router
from db.session import engine
from db.base import Base      # now import Base from db.base not db.base_class

...


def create_tables():
	print("create_tables")
	Base.metadata.create_all(bind=engine)

......
.....

```
Ok, time to restart the uvicorn server. Now, check your db tables. In case you are using SQLite use a tool named Downloads - DB Browser for SQLite (sqlitebrowser.org). 


