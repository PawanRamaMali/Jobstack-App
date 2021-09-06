##  Understanding Dependencies in FastAPI

Dependency injection is a beautiful concept. I won't torture you with big words, let's understand it with a simple example. You should be knowing that we use a test database to run our unit test and a production/development database. Can you imagine what would happen if we use the same database everywhere? Yes, our database will become a mess in few weeks! It would be filled up with useless emails like - test@example.com, mycutetest@test.com, and so on!

When we will be creating our logic to create a user, we would need to decouple our database settings and not hardcode it. During test, we would want a different database and during development/production our DB would be completely different and this can be achieved by using dependency injection. For this we would create a dependency called 'get_db' this would guide our database connection. During unit testing, we would override this 'get_db' dependency and we would get connected to some other test database. Now, I think you should have understood it to some extent. Now let's type in the below code in db > session.py


```py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator            #new


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

def get_db() -> Generator:   #new
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
 ```
 
 Done, now during testing, we would over-ride this 'get_db' to connect to a different database. 
