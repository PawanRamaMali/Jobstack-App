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
