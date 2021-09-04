# Jobstack-App

# Requirements

Install the requirements 

```
pip install -r requirements.txt
```

requirements.txt
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

.env 

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=yourdbname_eg_debug
```
