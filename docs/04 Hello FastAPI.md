
## Hello FastAPI

First of all, create a new folder inside of learning_fastapi directory, named backend.
Inside the backend, the directory make a requirements.txt file. In this requirements.txt file, we are going to keep track of all our project dependencies of external libraries. This is useful in case you share your code or you want to deploy it then the new system should know what all libraries our project needs. This is our current folder structure:

```
learning_fastapi/
├─.gitignore
└─backend/
  └─requirements.txt
  
```

Inside of requirements.txt file: type in the following:

```
fastapi
uvicorn
```

Fastapi you already know, uvicorn, hypercorn, gunicorn are servers that serve our API. I chose uvicorn because it supports async code. (Its not unicorn but uvicorn !)

To install these libraries type pip install -r requirements.txt in your terminal

It's time to taste fastapi, create a main.py file inside the backend folder, and type the following code, When I say type, I mean it, these are just 7-10 lines and you should type to get a better understanding of whats going on.

```py
#main.py

from fastapi import FastAPI
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)

@app.get("/")
def hello_api():
    return {"msg":"Hello API"}
    
```

Now, let's understand what we did, We are creating an instance of FastAPI and initializing it with a title and a project version. Now, we can reference the 'app' as a fastapi class object and use it to create routes.

* `@app.get('/')` is called a decorator. A decorator is used to provide extra functionality to a function. 
* `'/'` means that this is the home endpoint i.e. if our website example.com then this endpoint is for 'example.com'. Had it been '/about/' It would mean that whenever someone searches for example.com/about/, run this function.
* `get` here is called a verb. There are HTTP verbs that determine the functionality allowed for a request. In this case, get means "A user may connect to this home route to retrieve some information."


### More on HTTP verbs:

* GET:  Requests using GET should only retrieve data.

* POST: The POST method is used to submit an entity to the specified resource, e.g. submitting a form.

* PUT: The PUT method is used to update a database table record.

* DELETE: The DELETE method deletes the specified resource.

Okay back to our project. Notice that we are importing something from a config file from a folder named core.

```
├─.gitignore
└─backend/
  ├─core/
  │ └─config.py
  ├─main.py
  └─requirements.txt
  ```
  
We will store our project settings and configurations inside of this file named config.py.
  

```py
#config.py

class Settings:
    PROJECT_NAME:str = "Jobstack"
    PROJECT_VERSION: str = "1.0.0"

settings = Settings()
```

Ok now this is the moment, let's start the uvicorn server, type `uvicorn main:app --reload`

The --reload flag is to tell that 'uvicorn please auto-reload the application, every time I save any file on my project'. Now, visit http://127.0.0.1:8000/ you should see 

```
{"msg":"Hello API"}
```

Also, feel free to explore http://127.0.0.1:8000/docs.
