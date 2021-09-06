## Creating Schemas in Fastapi

A schema is used to validate data we receive as well as to reformat the data that we want to send to the client/browser. Suppose, we want to receive a JSON like {'username':'testuser','email':'testuser@nofoobar.com','password':'testing'} but there is no way we ca trust  our users. Our users may send anything they want and we don't want to store it without verifying. e.g. {'username':'testuser','email':'1234','password':'testing'} Notice here email is 1234, in such cases, we want to notify our users that we can't store such shit ! For this, we can go the hard way but we have Pydantic for our rescue. We create pydantic classes that verify the types and these classes are called Schemas. Let's jump into it and see it in action. Before that let's create files and folders to hold schemas.

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
│ ├─models/
│ │ ├─jobs.py
│ │ └─users.py
│ └─session.py
├─main.py
├─requirements.txt
├─schemas/          #new
│ ├─jobs.py         #new
│ └─users.py        #new
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
 
 Now, it's time to create the pydantic classes i.e. schemas. Let's start with users schemas. Type in the following code in schemas > users.py
 
 
```
from typing import Optional
from pydantic import BaseModel,EmailStr


#properties required during user creation
class UserCreate(BaseModel):
    username: str
    email : EmailStr
    password : str
    
```

Let's understand this dark magic! We are inheriting BaseModel from pydantic. It empowers fastapi to suggest validation errors to users. In this case, whenever we want to create a user, we will receive data in JSON format where the username will be verified to be a string, the email will be verified to be in proper mail format and the password will be validated to be a string.

Because we are trying to use EmailStr from pydantic we need to install this service first. Let's add pydantic[email] to our requirements.txt file and install all requirements by pip install -r requirements.txt.

```
# previous requirements here ...
# ....
# .... 

#for loading environment variables
python-dotenv

#for email validation            #new
pydantic[email] 

```

Schemas will be clearer when we will use schemas in our routes.
