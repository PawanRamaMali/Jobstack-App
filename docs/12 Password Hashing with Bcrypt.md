
## Password Hashing with Bcrypt


Storing raw passwords is super dangerous. In case our db is compromised for whatsoever reason. All our user's passwords will be available to the hacker without any effort. To tackle this scenario we make use of password hashing. In very simple words, It is a one-way algorithm to convert passwords to a string that looks like gibberish e.g. If your password is "HelloWorld" it would become $2y$12$kbQm9Vb96023efZFhSkZf.a4bAGyzDW6zKC/K1JDtKY0f.gKZxAHO with 12 cryptographic iterations. I would suggest playing with Bcrypt Generator to get a feel of hashing. The wonderful thing about hashing is that we do not de-hash but we compare hashes to see if the password entered is the same as that of the existing password.
There are many hashing algorithms like PBKDF2, SHA1, SHA256, and many more. In this post, we are going to use the BCrypt algorithm. We will be using a super library passlib, to handle hashing and comparison for us. So, let's install passlib along with Bcrypt. Update your requirements.txt file with passlib[bcrypt] and do a pip install -r requirements.txt.

```
fastapi
uvicorn

#for template
jinja2

#for static files
aiofiles

#for database
sqlalchemy
psycopg2

#for loading environment variables
python-dotenv

#for email validation
pydantic[email]

#hashing              #new
passlib[bcrypt]
```

Now, we are going to create a file in which we will be implementing the class to handle Hashing. Make a new file inside the core folder named hashing.py.   Core > hashing.py and paste the following lines.


```py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)
        
 ```
 
*  We are creating  static methods. A static method is one which does not requires to be called using the instance/object of the class. We can directly call these methods like 'Hasher.verify_password'. 
* I made the methods static because there was no need for it to be called by an object. Object creation would have been a redundant thing. Now, you might question then why I wrapped these functions inside Hasher class? Ya that's a valid question. I did it to be more explicit while calling the verify password function. It is easier to understand Hasher.verify_password and similar methods stay connected or wrapped together.
* Ok let's try it out on shell. Type "python" or "python3" in terminal or your cmd and press Enter and explore our new hasher.

![image](https://user-images.githubusercontent.com/11299574/132249230-084438ae-b186-4f9d-ac78-db7dafae4525.png)



 
