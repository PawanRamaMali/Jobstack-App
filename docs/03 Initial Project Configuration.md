## Initial Project Configuration

Have a virtualenv: First things first, We need a virtual environment, A virtual environment is like a separate space wherein we can install our project requirements which is completely isolated from the global installations. Years back, When I was starting with Django, I used to install some requirements for some project(x) e.g. 

```
django==2.2
requests
email-validator==1.8.1
....
```

and after some days I would switch to some other project for some time. When I would come back to the original project (x), It would not work and strange errors would come. Later, I learned that I was always messing with the global installation.😄 

So, make a project directory(folder) and cd into it. To make a virtual environment type the command: 

```
#cd to the folder learning_fastapi

python -m venv env
#env is the name of virtual env
```

now activate the virtual environment. If you are in windows use `.\env\Scripts\activate` Linux guys use  `. env/bin/activate`

## Initializing Git:

One more thing is we will be using git for version control. Version control is used mainly to do development in separate branches kind of virtual environment for code! and to merge when the development of one feature is complete. It is also the Docter strange for our application. If something breaks then we can revert our code to some previous state.

Type the below command, make sure you are in the learning_fastapi directory in terminal/cmd.

`git init`

Refer to the following screenshot in case you are confused, otherwise, you are good to go

## Knowing what to ignore!

This mistake I used to do a lot when I started with development. I used to put my code to GitHub but I did not know about the .gitignore thing and I used to send my virtualenv, SQLite DB, even once or twice the secret file which had the secret key of my AWS s3 instance, Mailchimp secret key. Then, all of my accounts were closed by the AWS team and I had to again configure all of that. Yup, I am a fool, and it's common to make mistakes, but the moral is to learn from it. So, I advise you to create a .gitignore file inside of the "learning_fastapi" directory and inside of this `.gitignore` file. Copy the below lines and save.

```
__pycache__
.env
env
test_db.db
```

These lines simply mean that "git doesn't send over these files to GitHub". __pycache__ is to ignore the binary files which are created by python.
