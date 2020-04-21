# Endpoints documentation

1. [Posts](#posts)
    - [Reading by serial](#reading-by-serial)
        - [Reading public posts](#public-posts)
        - [Reading encrypted posts](#encrypted-posts)
    - [Dumping posts](#dumping-posts)
        - [Dump all](#dump-all-posts)
        - [Dumping by author](#dumping-by-author)
        - [Dumping by category](#dumping-by-category)
    - [Creating](#creating)
    - [Updating](#updating)
    	- [Updating public posts](#updating-public-posts)
        - [Updating encrypted posts](#updating-encrypted-posts)
2. [Users](#users)
    - [Account](#account)
        - [Registering new accounts](#register)
        - [Logging in](#login)
        - [Update user information](#edit-user-by-uuid)
    - [Tokens](#tokens)
        - [Refresh tokens](#refresh-tokens)
        - [Access token with Fresh status](#fresh-token)
    - [Dumping users](#dumping-users)
        - [Dump all](#dump-all-users)
        - [Dump by UUID](#dump-by-uuid)
3. [Articles](#articles)

# Posts
This category handles all the thing related to reading/creating/updating/deleting content from the database. The methods support AES encryption. All of the requests take in and reponde with **JSON** data. 

## Reading by serial
Here I will define the serial termen, and others if is needed.
- `serial` is a way of indexing data, wich can handle up to 36 at 8th power different variables. It can only contain lower ascii letters (a-z) and all digits(0-9). This can not be changed anytime, so it's bound to the post (it doesn't matter that the title or author changes) all the time.
- 'encryptionKey' is used for the encryption algorithm (AES) and it must be different for each encryption. This is stored in the database as a BCRYPT hash, for security purposes. Even if the databases is breached, all the content is secure.

### Public posts
- **Description**: You can read posts by it's serial attribute, look up at the [serial definition](#reading-by-serial). You will retrieve only one post from this method and it must not have the status 'encrypted'.  
- **Endpoint**: `/post/<serial>`
- **Method**: GET
- **Body**: None
- **Reponses**:
Example:
```json
200: 
{
    "data": {
        "title": "Public second user third post",
        "author": {
            "username": "test",
            "uuid": "2d9c26cd-68d6-4bed-9434-55017b15dc3a",
            "activity": 3,
            "id": 1,
            "email": "test@test.ro"
        },
        "id": 1,
        "status": "public",
        "date": "2020-04-20T20:31:03",
        "content": "Lore Ipsum",
        "author_id": 1,
        "serial": "q8qvm84r",
        "category": "API"
    }
}
400: {"message": "This is an encrypted post. To read it's content you must pass the encryption key"} (Bad request)
404: {"message": "There is no post with this serial. Please recheck."} (Not found)
```
### Encrypted posts
- **Description**: You can read encrypted posts by it's serial attribute, look up at the [serial definition](#reading-by-serial). You need to pass the original encryption key to decode it.
- **Endpoint**: `/post/<serial>/<key>`
- **Method**: GET
- **Body**: None
- **Reponses**:
> The reponse is the same for 200, as in the [Reading public posts](#public-posts)
```json
200:
{
    "data": {
        "title": "Lol? New post",
        "author": {
            "username": "test",
            "uuid": "2d9c26cd-68d6-4bed-9434-55017b15dc3a",
            "activity": 3,
            "id": 1,
            "email": "test@test.ro"
        },
        "id": 2,
        "status": "encrypted",
        "date": "2020-04-21T01:00:24",
        "content": "Lore ipsum is just for testing the AES encryption. ",
        "author_id": 1,
        "serial": "ysxtdnxl",
        "category": "API"
    }
}
400: {"message": "This post is not encrypted. Everyone can read it."}
401: {"message": "That's the wrong key. We can't decrypt the message."}
404: {"message": "There is no post with this serial. Please recheck."}
```

## Dumping posts
With the help of this endpoint you can dump the whole posts from the database, or you can add filters. 
> Note: Both encrypted & public posts will be dumped. 
### Dump all posts
- **Description**: You can dump all the posts from our database. They are sorted by the last created at the time of request. 
- **Endpoint**: `/posts/all`
- **Method**: GET
- **Body**: None
- **Reponses**:
Example: 
```json
200: 
{
    "count": 1,
    "data": [
        {
            "title": "Secured data. Key Only!",
            "author": {
                "username": "test",
                "uuid": "2d9c26cd-68d6-4bed-9434-55017b15dc3a",
                "activity": 3,
                "id": 1,
                "email": "test@test.ro"
            },
            "id": 3,
            "status": "encrypted",
            "date": "2020-04-21T01:07:45",
            "content": "dGlMCc/faqNL0OPfeqspGg==:5JI7VTbuIqrHe2PZFRkEZA==",
            "author_id": 1,
            "serial": "i07z2sbq",
            "category": "API"
        }
    ]
}
404: {"message": "There are no posts yet."}
```

### Dumping by Author
- **Description**: You can dump all the posts from the same author. They are sorted by the last created at the time of request. 
- **Endpoint**: `/posts/author/<name>`
- **Method**: GET
- **Body**: None
- **Reponses**:
Example: 
```json
200: 
{
    "count": 1,
    "data": [
        {
            "date": "2020-04-21T01:07:45",
            "title": "Secured data. Key Only!",
            "status": "encrypted",
            "category": "API",
            "author": {
                "email": "test@test.ro",
                "activity": 3,
                "username": "test",
                "uuid": "2d9c26cd-68d6-4bed-9434-55017b15dc3a",
                "id": 1
            },
            "serial": "i07z2sbq",
            "id": 3,
            "content": "dGlMCc/faqNL0OPfeqspGg==:5JI7VTbuIqrHe2PZFRkEZA==",
            "author_id": 1
        }
    ]
}
404: {"message": "This author didn't posted yet."}
```

### Dumping by Category
- **Description**: You can dump all the posts from the same category. They are sorted by the last created at the time of request. 
- **Endpoint**: `/posts/category/<name>`
- **Method**: GET
- **Body**: None
- **Reponses**:
Example:
```json
200: 
{
    "count": 1,
    "data": [
        {
            "serial": "i07z2sbq",
            "author": {
                "email": "test@test.ro",
                "uuid": "2d9c26cd-68d6-4bed-9434-55017b15dc3a",
                "activity": 3,
                "id": 1,
                "username": "test"
            },
            "author_id": 1,
            "content": "dGlMCc/faqNL0OPfeqspGg==:5JI7VTbuIqrHe2PZFRkEZA==",
            "status": "encrypted",
            "id": 3,
            "title": "Secured data. Key Only!",
            "category": "API",
            "date": "2020-04-21T01:07:45"
        }
    ]
}
404: {"message": "There are no posts in this category yet."}
```

## Creating
With this endpoint, you can add different posts in our database. For security resons we will check if the author is in our database and if he is makeing the request. 
> Note: If you want to encrypt a post from this stage, setting the [`encryptionKey`](#reading-by-serial) will be enough. The status will be overwritten by default to `encrypted` when you have that parameter.  

- **Endpoint**: `/post`
- **Method**: POST
- **Securiy**: This method requires a security header `Authorization: Bearer {access_token}`, which you can get at [logining in](#login) or at [refreshing](#refresh-tokens). Any `access token` that is valid will be accepted.
- **Body**: 
Creating a public post, without encryption
```JSON
{
	"status": "public",
	"category": "API",
	"content": "Lore Ipsum",
	"title": "Public second user third post"
}
```
Creating an encrypted content
```JSON
{
	"status": "encrypted",
	"category": "API",
	"content": "Lore ipsum",
	"title": "Secured data. Key Only!",
	"encryptionKey": "x60ad5d46d54665b50466a939bff1b35"
}
```
- **Reponses**:
```JSON
201: {"message": "Post created with serial <serial>."} 
401: {"msg": "Token has expired"}
401: {"msg": "Missing Authorization Header"}
500: {"message":"Something went wrong. We can't upload this in our database."}
```

## Updating
If you want to make some changes you can just find and update them using the post's [serial](#reading-by-serial) code. We will have two methods, because we are working with encrypted and public content.
> Note: With this method you can change the status of the content ( For example if you want to transform an `encypted` post to  `public` and vice versa. )

### Updating public posts
- **Description**: With this method you can only change the Title, Content, Status and Category. By changing the `status` you can also encrypt the posts. If the post is encrypted you might want to look into [Updating encrypted posts](#updating-encrypted-posts)
- **Endpoint**: `/posts/<serial>`
- **Method**: PUT
- **Securiy**: This method requires a security header `Authorization: Bearer {access_token}`, which you can get at [logining in](#login) or at [refreshing](#refresh-tokens). Any `access token` that is valid will be accepted. 
- **Body**: 
This is just for updating a regular post
```JSON
{
	"status": "public",
	"category": "API",
	"title": "Lol? New post",
	"content": "Lore ipsum"
}
```
And this is how you encrypt a public post with this method. Parameter `encryptionKey` is a must and it can be empty. Without him it will throw an error. Note that you can only pass `status` and `encryptionKey` to do the encryption. 
```JSON
{
	"status": "encrypted",
	"category": "API",
	"title": "Encrypting with AES",
	"content": "Lore ipsum",
	"encryptionKey": "s3cur3@K3y"
}
```
- **Reponses**:
```json
200: {"message": "Post with serial `<serial>` has been updated in our database"}
400: {"message": "To make any changes to this post you must pass the encryption key."}
400: {"message": "You don't have the encryptionKey. We can't encrypt a message without it."}
401: {"msg": "Token has expired"}
401: {"msg": "Missing Authorization Header"}
404: {"message": "There is no post with this serial. Please recheck."}
500: {"message": "There was an error with the encryption. Try again."}
500: {"message":"Something went wrong. We can't upload this in our database."}
```
### Updating encrypted posts
- **Description**: With this method you can only change the Title, Content, Status and Category. By changing the `status` you can also decrypt the posts. If the post is not encrypted you might want to look into [Updating public posts](#updating-public-posts)
- **Endpoint**: `/posts/<serial>/<key>`
- **Method**: PUT
- **Securiy**: This method requires a security header `Authorization: Bearer {access_token}`, which you can get at [logining in](#login) or at [refreshing](#tokens). Any [access token](#token) that is valid will be accepted.
- **Body**: 
This is just for updating a regular encrypted post, all these fields are optional. You can update only one at a time. 
```JSON
{
	"title": "This is a test",
	"content": "Lore ipsum",
	"category": "API"
}
```
And this is how to decrypt this post. The `status` can be anything else. This is the check: `data.status != 'encrypted'`
```JSON
{
	"status": "public"
}
```
- **Reponses**:
```json
200: {"message": "Post with serial `<serial>` has been updated in our database."}
400: {"message": "This post is not encrypted. Everyone can read it."}
401: {"message": "This is the wrong key. We can't decrypt the message, so you can't edit it."}
401: {"msg": "Token has expired"}
401: {"msg": "Missing Authorization Header"}
404: {"message": "There is no post with this serial. Please recheck."}
500: {"message":"Something went wrong. We can't upload this in our database."}
```

# Users
This subset of URL's contains Authentification & Authorization for the **Security** tags found in other models. In order to keep the code clean we decided to use JWT tokens. Those are signed with a `Secret key` which is very hard to bruteforce, so the signiture can't be randomly modified. With the help of this module we are able to keep track of the active users on our platform.


## Account
This section will cover everything related to users, Registration, Login and Updating information. There are a few mentions about tokens in here.
- **passwords**: In order to validate a `password` it must have a length between 8 and 64 
> Note: The password used (`justAt3stp@ass`) is not a default, generated by server one. There is no thing as `default user` with this password, it's just for demonstration purposes. 

### Register
- **Description**: This method is just for adding new users to our database. There are a few restrictions, username and email must be unique, and it will output the specific UUID if the response is 201.
- **Endpoint**: `/users/register`
- **Method**: POST
- **Securiy**: None
- **Body**:
```json
{
	"username": "test",
	"email": "test@test.ro",
	"password": "justAt3stp@ass"
}
```
- **Reponses**:
```
201: {"message": "User with uuid `<uuid>` has registered successfully"}
400: {"message": "A password must have between 8 and 64 characters long and it must contain letters (uppercase and lowercase) and digits."}
401: {"message": "This username already exists in our database. Try to login or reset the password"} 
401: {"message": "This email already exists in our database. Try to login or reset the password"}
```

### Login 
- **Description**: Passing username and password will provide you with a 15 minute valid [access_token](#tokens) with fresh status and 1 month [refresh_token](#tokens). 
- **Endpoint**: `/users/login`
- **Method**: POST
- **Securiy**: None
- **Body**:
```json
{
	"email": "test@test.ro",
	"password": "justAt3stp@ass"
}
```
- **Reponses**:
```json
200:
{
    "message": "Successfuly logged in!",
    "access_token": "{access_token with Fresh status}",
    "refresh_token": "{refresh_token}"
}
401: {"message": "Invalid credentials!"}
404: {"message": "This user doesn't exist in our database."}
```

### Edit user by UUID 
- **Description**: Here you can update the email, password and other details related to the account. For this you will need a token with the [fresh](#tokens) attribute.
- **Endpoint**: `/users/edit/<uuid>`
- **Method**: PUT
- **Securiy**: `Authorization: Bearer {{access_token}}`, token with [fresh=True](#tokens) attribute
- **Body**: In future versions there will be other things to edit.
```json
{
	"email": "",
	"password":""
}
```
- **Reponses**:
```json
200: {"message": "There is nothing to change in here."}
201: {"message": "Changes have been updated in our database."}
400: {"message": "This email is already linked to another account."}
400: {"message": "You can't change the password with the old one."}
400: {"message": "A password must have between 8 and 64 characters long and it must contain letters (uppercase and lowercase) and digits."}
404: {"message": "This user doesn't exist anymore!"}
500: {"message": "There was an error on our system and we can't save this to our database. Try again"}
```

## Tokens
I will go more in depth here what's with that `access_token` and `refresh_token`, including the fresh statute of those.
- `Access tokens`: These tokens can be generated with two different statutes: Fresh or not. First of all, an access_token can be generated either by a fresh login, or by using the refresh_tokens. In order to get a token with status `Fresh=True` you will need to pass the password along with the refresh token. The length of these tokens is `15 minutes`.
- `Refresh tokens`: They are passed first at login and they can last up to one month. Their only purpose is to renew the access_tokens. Passing a password along with this tokens will result in generating `Fresh tokens` ( access and refresh )
- `Fresh tokens` : These tokens can only be obtained by passing user credentials (at login) or at least the password associeted with the UUID stored in the `refresh_token`. There are a few places where you will need this kind of token, those being mentioned in the **Security** tag.

### Refresh tokens
- **Description**: With this method you can generate a new `access_token`, but without the fresh statute. 
- **Endpoint**: `/users/refresh`
- **Method**: GET
- **Securiy**: `Authorization: Bearer {{refresh_token}}`
- **Body**: None 
- **Reponses**:
```json
200:
{
    "message": "You got a new access token!",
    "access_token": "<token>"
}
422: {"msg": "Only refresh tokens are allowed"}
```

### Fresh tokens
- **Description**: With this method you can generate a new `access_token` as well as `refresh_token`, but with the fresh statute. 
- **Endpoint**: `/users/refresh/login`
- **Method**: POST
- **Securiy**: `Authorization: Bearer {{refresh_token}}`
- **Body**:
```json
{
	"password": "justAt3stp@ass"
}
```
- **Reponses**:
```json
200:
{
    "message": "Access granted. You have renewed you session",
    "access_token": "<access_token with Fresh=True>",
    "refresh_token": <refresh_token>"
}
422: {"msg": "Only refresh tokens are allowed"}
```

## Dumping Users
Found as well in the `Posts` module, this just dump users, and it accept filters.

### Dump all Users
- **Description**: This will display all users that are curently in our database.
- **Endpoint**: `/users/dump`
- **Method**: GET
- **Securiy**: `Authorization: Bearer {{access_token}}`
- **Body**: None
- **Reponses**:
```json
200: 
{
    "count": 1,
    "data": [
        {
            "email": "test@test.ro",
            "activity": 3,
            "username": "test",
            "uuid": "2d9c26cd-68d6-4bed-9434-55017b15dc3a",
            "id": 1
        }
    ]
}
404: {"message":"There are no users registered yet."}
Others error messages are related to security ( validity of JWT Tokens )
```

### Dump by UUID
- **Description**: This will always return only one user, the one identified by his UUID
- **Endpoint**: `/users/dump/<uuid>`
- **Method**: GET
- **Securiy**: `Authorization: Bearer {{access_token}}`
- **Body**: None
- **Reponses**: 
- **Reponses**:
```json
200: 
{
    "data": {
        "email": "test@test.ro",
        "id": 1,
        "uuid": "2d9c26cd-68d6-4bed-9434-55017b15dc3a",
        "activity": 3,
        "username": "test"
    }
}
}
404: {"message": "There is no user with the specified UUID."}
Others error messages are related to security ( validity of JWT Tokens )
```

# Articles
- [List of HTTP status codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes)
