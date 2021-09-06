## Our First FastAPI Route 

 Till now we have made very simple routes, This time we will be using pydantic schemas, database connections, dependencies all at one endpoint. We are going to make a route which will enable creation of users. Why are we doing this first? Its because in our 'Job' model, we have a foreign key to the users table. So, we need an owner_id which is basically id of an user model. Lets jump into the code but before that create this new folder structure:
 
 ```
 backend/
├─.env
├─apis/
│ ├─base.py                   #new file
│ └─version1/                 #new folder
│   ├─route_general_pages.py    #new
│   └─route_users.py            #new
├─core/
│ ├─config.py
│ └─hashing.py
├─db/
│ ├─base.py
│ ├─base_class.py
│ ├─models/
│ │ ├─jobs.py
│ │ └─users.py
│ ├─repository/                 #new
│ │ └─users.py                  #new
│ └─session.py
├─main.py
├─requirements.txt
├─schemas/
│ ├─jobs.py
│ └─users.py

```

Copy everything from general_pages > route_homepage.py to version1 > route_general_pages.py
Now, we need to type the below lines in apis > version1 > route_users.py

```py
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

from schemas.users import UserCreate
from db.session import get_db
from db.repository.users import create_new_user

router = APIRouter()


@router.post("/")
def create_user(user : UserCreate,db: Session = Depends(get_db)):
    user = create_new_user(user=user,db=db)
    return user
```

* We will receive a post request at this endpoint.
* create_user function will receive user from request and UserCreate schema will validate that it has a username,email in proper format, and a password.
* We will get the database session using the dependency get_db that we made in session.py file.
* We are again calling a completely new function named create_new_user and passing the user data from request and database session.
* Here we are trying to follow a design pattern named repository pattern. In this way, our code that interacts with the database is completely separated from this route. In the future, If we want to use some other ORM e.g. Tortoise or Pweee then it will become easier as the ORM code is completely separated from the route. The responsibility of user creation is passed on to the create_new_user function so let's implement it.

Type the following in db > repository > users.py


```py
from sqlalchemy.orm import Session

from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher


def create_new_user(user:UserCreate,db:Session):
    user = User(username=user.username,
        email = user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_superuser=False
        )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
    
 ```
 
 * Now we need to include the router in route_users.py file to our app in main.py file. But think of it, if we have 100 routers, should we import and include 100 routes in main.py file? No, it will get cluttered, so, I am going to make a new router in apis > base.py file which will contain the information of other routers. Put the following code in apis > base.py

```py
from fastapi import APIRouter

from apis.version1 import route_general_pages
from apis.version1 import route_users


api_router = APIRouter()
api_router.include_router(route_general_pages.general_pages_router,prefix="",tags=["general_pages"])
api_router.include_router(route_users.router,prefix="/users",tags=["users"])

```
Just one step more, make sure we import this 'api_router' in main.py file and include with our app: main.py


```py
from core.config import settings
from apis.base import api_router #new
from db.session import engine
from db.base import Base 


def include_router(app):   
	app.include_router(api_router) #modified


..
...
...

```

But there is a problem with this approach, Just look at all the data we are showing to our users. 

We are passing hashed_password, id, and is_superuser status, These are implementation details and from a security point of view, we should not pass these data. Let's restrict our response to only username, email and is_active status. Remember pydantic schemas? They are used to validate request data. Similarly, they can be used to restrict data to have only a limited number of fields.
Let's add a new schema in schemas > users.py

```py
from typing import Optional
from pydantic import BaseModel,EmailStr


#properties required during user creation
class UserCreate(BaseModel):
    username: str
    email : EmailStr
    password : str


class ShowUser(BaseModel):   #new
    username : str 
    email : EmailStr
    is_active : bool

    class Config():  #tells pydantic to convert even non dict obj to json
        orm_mode = True
        
```


and we need to specify this ShowUser schemas as a response_model of our post route. I believe it would be better to call it request_schema!!  Ok, now we modify our apis > version1 > route_users.py as follows:


```py
...

from schemas.users import UserCreate,ShowUser  #modified
from db.session import get_db
...

router = APIRouter()


@router.post("/",response_model = ShowUser)          #modified
def create_user(user : UserCreate,db: Session = Depends(get_db)):
    user = create_new_user(user=user,db=db)
    return user 
    
```

All done, now we are not passing hashed_password, id, etc. 
