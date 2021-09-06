## Unit Testing FastAPI Routes


Is TDD important ? Without a second thought, I would say yes, In our company codebase we have around 1400+ unit tests. Just 2 years before, We were literally fearful each time we had to release a new feature. Because If I make one single change in the Users table, I don't know which part of our codebase may break! I use unit tests mostly for a single purpose. It works as documentation from my side, By designing a unit test I tell fellow developers, how exactly this new feature should work.

Ok enough talk, I don't want to bore you by just talking. So, let's jump into it. We need to create some files and folders:

```
backend/
├─.env
├─apis/
│ ├─base.py
│ └─version1/
│   ├─route_general_pages.py
│   └─route_users.py
├─core/
│ ├─config.py
│ └─hashing.py
├─main.py
├─requirements.txt
├─templates/
│ ├─components/
│ │ └─navbar.html
│ ├─general_pages/
│ │ └─homepage.html
│ └─shared/
│   └─base.html
├─tests/            #new
│ ├─conftest.py     #new
│ └─test_routes/    #new
│   └─test_users.py #new

```

We also need pytest and requests for testing our APIs. So, let's modify our requirements.txt file and do a pip install -r requirements.txt to install these.


```
#requirements.txt file
...
...

#for email validation
pydantic[email]

#hashing
passlib[bcrypt]


#for testing       #new
pytest
requests

```

Now, we will add configurations for testing. Paste the following lines in tests > conftest.py

```py
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#this is to include backend dir in sys.path so that we can import from db,main.py

from db.base import Base
from db.session import get_db
from apis.base import api_router


def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
 
```


* Woah, this is too much torture. But if you read this file you will understand 90% of the things. Give it a try.
* We are creating a new Fastapi instance, app, and a brand new database. This is an SQLite database and we don't  need to do anything because python will create a file - test_db.db
* We are doing this because we don't want to mess up our original database with test data. Just imagine 100s and 1000s of emails like 'test@nofoobar.com" !
* Now the big question is, Will fastapi use this test db, if yes then how? Remember the concept of dependencies that we studied in the previous post. The good thing is we have not hardcoded the database to be used in the routes. We are making use of a dependency named 'get_db' to provide a database session.
* In our unit tests, we will be overriding this dependency and provide our test database instead. This concept is known as dependency injection.
* There is a rule that each test should be independent. So, we are resetting/rollbacking the changes in the db tables and even creating a new database for each test! By, the way rollback would be sufficient 😅

Now, we can make unit tests, Notice we have made 'client' as a module-level test fixture. So, by using this client we would be able to rollback things and keep our tests isolated and independent. Type the below code in tests > test_routes > test_users.py


```py
import json


def test_create_user(client):
    data = {"username":"testuser","email":"testuser@nofoobar.com","password":"testing"}
    response = client.post("/users/",json.dumps(data))
    assert response.status_code == 200 
    assert response.json()["email"] == "testuser@nofoobar.com"
    assert response.json()["is_active"] == True
    
```

Done, now type pytest in the terminal/cmd and see the magic !

