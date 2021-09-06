## Serving HTML with FastAPI

If someone hits our home/index endpoint they won't understand anything. So, the template is necessary.

We will be using Jinja as our templating language. Before that, we need to make some folders and files. Notice the below folder structure of mine, the names 'apis/', 'templates/' are ending with a '/', so these are folders and others are simple .py or .html files. I have added a comment '#new' for the new files and folders that need to be created.

```
learning_fastapi/
├─.gitignore
└─backend/
  ├─apis/  #new
  │ └─general_pages/ #new
  │   └─route_homepage.py  #new
  ├─core/
  │ └─config.py
  ├─main.py
  ├─requirements.txt
  └─templates/  #new
    ├─components/  #new
    │ └─navbar.html  #new
    ├─general_pages/  #new
    │ └─homepage.html  #new
    └─shared/   #new
      └─base.html   #new

```
Now, enter the below lines in 'route_homepage.py'.


```py
#route_homepage.py

from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
general_pages_router = APIRouter()


@general_pages_router.get("/")
async def home(request: Request):
	return templates.TemplateResponse("general_pages/homepage.html",{"request":request})
	
```


* We imported the necessary modules.
* We created an object of Jinja2Templates and instantiated it with directory/folder name templates. So, now Jinja2 understands that it has to search for HTML files inside the templates folder.
* we created an instance of APIRouter named general_pages_router. But why? We could have kept all this code in the main.py file but as our codebase grows we will find it to be messy. So, we are trying to keep our codebase clean from the beginning and so, we are utilizing the APIRouter of fastapi.
* Next is a home function, we have made it async but don't concentrate too much on it. We will learn it later. It is not necessary for this function. In this function, we are basically capturing the actual request and returning an HTMLResponse with the request in a dictionary. This dictionary is called a context dictionary. 
* Always learn to ask why. Why are we capturing request and passing it in the context dictionary. The answer lies in request only, If we add a print statement print(dir(request)) ,we see that request has many important attributes like 'user','cookies', 'form', 'get', 'headers', 'path_params', 'query_params',  ' 'url','url_for','values' which might be used in templates. E.g. It is very common to use request.user in template file.

Next, we need to concentrate on homepage.html. Copy the below code in this file.

```
{% extends "shared/base.html" %}


{% block title %} 
  <title>Job Board</title>
{% endblock %} 

{% block content %} 
  <div class="container">
    <h1 class="display-4">Find Jobs...</h1>
  </div>
{% endblock %} 

```

* I am using template inheritance here. Basically, there is some base.html file that has some empty blocks/space. We are asking jinja to find the base.html file and insert the code in the block of homepage to block inside base.html.
* But why am I complicating all of this? This I am doing to follow the DRY(Don't Repeat Yourself) principle. There are some common lines which we don't need to write again and again. Consider bootstrap cdn links, we are going to use bootstrap for all the html, So, why to keep these links on all the pages. So, we have base.html which will be shared by other HTML files.

This is our base.html file.

```html
<!DOCTYPE html>
<html lang="en-us">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="fastapitutorial.com" content="Nofoobar">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">

    {% block title %}
    {% endblock %}
</head>

<body>
    {% block content %}
    {% endblock %}

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script>
    {% block scripts %}
    {% endblock %}


</body>
</html>
```

Done? No! there are still some things left. One is our main.py file has app, which does not know about all of these. So, we are going to inform our main.py file to include this general_pages_router.

```py
#main.py 

from fastapi import FastAPI
from core.config import settings
from apis.general_pages.route_homepage import general_pages_router


def include_router(app):
	app.include_router(general_pages_router)


def start_application():
	app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
	include_router(app)
	return app 


app = start_application()


# @app.get("/") #remove this, It is no longer needed.
# def hello_api():
#     return {"msg":"Hello API"}

```

Ok, one last thing, I promise last. We don't have Jinja2, So, add the below line in requirements.txt:

```
fastapi
uvicorn


#for template  #new
jinja2 

```
Now, install Jinja2 like with pip install -r requirements.txt. All done, now start the server with uvicorn main:app --reload and visit http://127.0.0.1:8000/. You should see a template response.


