##  Serving Static Files with FastAPI

When we fill a form, say a form that asks for an image upload from a computer. Then the image uploaded by us is called a media.
But when a webpage shows us an image or provides CSS, js file to the browser, it's a static file. Ok, now lets add a our logo to navbar. For serving static files, we will make use of a library named aiofiles. Lets add this to our requirements.txt file.

```
fastapi
uvicorn


#for template
jinja2


#for static files
aiofiles

```
Now, install aiofiles with pip install -r requirements.txt. Now, since this static files configuration is not specific for a particular route, I am going to modify our main.py file to support static files.

```py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles #new
from core.config import settings
from apis.general_pages.route_homepage import general_pages_router


def include_router(app):
    app.include_router(general_pages_router)


def configure_static(app):  #new
    app.mount("/static", StaticFiles(directory="static"), name="static")


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app) #new
    return app

app = start_application()
```

Basically, we are informing fastapi that we are going to keep all our static files in a folder named 'static' and whenever it has to search for a static file, say an image, don't search here and there. It will be inside static folder only.

Ok, this part is complete, now lets put an image in the path static > images > logo.png.

```
backend/
├─apis/
│ └─general_pages/
│   └─route_homepage.py
├─core/
│ └─config.py
├─main.py
├─requirements.txt
├─static/         #new
│ └─images/       #new
│   └─logo.png    #new
└─templates/
  ├─components/
  │ └─navbar.html
  ├─general_pages/
  │ └─homepage.html
  └─shared/
    └─base.html
    
```
To include a static file in template we make use of url_for template tag. e.g. 

<img src="{{ url_for('static', path='images/jb.png') }}" alt="" width="30" height="24">

<link href="{{ url_for('static', path='/styles.css') }}" rel="stylesheet">
Ok, now let's modify our navbar.html file to have a brand image.

```html
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">
      <img src="{{ url_for('static', path='images/logo.png') }}" alt="" width="30" height="24">
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Link</a>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Dropdown
          </a>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
            <li><a class="dropdown-item" href="#">Action</a></li>
            <li><a class="dropdown-item" href="#">Another action</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">Something else here</a></li>
          </ul>
        </li>
        <li class="nav-item">
          <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
        </li>
      </ul>
      <form class="d-flex">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
    </div>
  </div>
</nav>

```
Now, you should have a logo in the navbar.

