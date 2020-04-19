# Endpoints documentation

1. [Posts](#posts)
    - [Reading by serial](#reading-by-serial)
        - [Reading public posts](#public-posts)
        - [Reading encrypted posts](#encrypted-posts)
    - [Dumping posts](#dumping-posts)
        - [Dump all](#dump-all)
        - [Dumping by author](#dumping-by-author)
        - [Dumping by category](#dumping-by-category)
    - [Creating](#creating)
    - [Updating](#updating)
    	- [Updating public posts](#updating-public-posts)
        - [Updating encrypted posts](#updating-encrypted-posts)
2. [Articles](#articles)

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
    "data": {
        "id": 1,
        "author": "wh0ami",
        "serial": "9js01a3l",
        "category": "Information",
        "date": "2020-04-14T22:51:30",
        "status": "public",
        "title": "Is this encryption?",
        "content": "Trying to not encrypt the text"
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
200: "data": <JSON Object>
400: {"message": "This post is not encrypted. Everyone can read it."}
401: {"message": "That's the wrong key. We can't decrypt the message."}
404: {"message": "There is no post with this serial. Please recheck."}
```

## Dumping posts
With the help of this endpoint you can dump the whole posts from the database, or you can add filters. 
> Note: Both encrypted & public posts will be dumped. 
### Dump All
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
            "id": 6,
            "author": "wh0am1",
            "serial": "ow7bpkbh",
            "category": "Informations",
            "date": "2020-04-19T21:02:23",
            "status": "encrypted",
            "title": "AES encryption be like...",
            "content": "p2mlZ:EsrI0i0PvDg2eoO8tzAyk88qA1xxuG+n5HDYMIcOuKwfFWMFTwtM="
        }
  ]
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
    "count": 2,
    "data": [
        {
            "id": 6,
            "author": "wh0am1",
            "serial": "ow7bpkbh",
            "category": "Informations",
            "date": "2020-04-19T21:02:23",
            "status": "encrypted",
            "title": "AES encryption be like...",
            "content": "I had to cut it, because it was to long."
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
            "id": 1,
            "author": "wh0ami",
            "serial": "9js01a3l",
            "category": "Information",
            "date": "2020-04-14T22:51:30",
            "status": "public",
            "title": "Is this encryption?",
            "content": "Trying to not encrypt the text"
        }
    ]
}
404: {"message": "There are no posts in this category yet."}
```

## Creating
With this endpoint, you can add different posts in our database. 
> Note: If you want to encrypt a post from this stage, setting the [`encryptionKey`](#reading-by-serial) will be enough. The status will be overwritten by default to `encrypted` when you have that parameter.  

- **Endpoint**: `/post`
- **Method**: POST
- **Body**: 
Creating a public post, without encryption
```JSON
{
	"author": "wh0am1",
	"status": "public",
	"category": "API",
	"content": "Lore Ipsum",
	"title": "Public data for everyone"
}
```
Creating an encrypted content
```JSON
{
	"author": "wh0am1",
	"status": "encrypted",
	"category": "API",
	"content": "Lore ipsum",
	"title": "Secured data. Key Only!",
	"encryptionKey": "s3cur3@K3y"
}
```
- **Reponses**:
```JSON
201: {"message": "Post created with serial <serial>."} 
500: {"message":"Something went wrong. We can't upload this in our database."}
```

## Updating
If you want to make some changes you can just find and update them using the post's [serial](#reading-by-serial) code. We will have two methods, because we are working with encrypted and public content.
> Note: With this method you can change the status of the content ( For example if you want to transform an `encypted` post to  `public` and vice versa.

### Updating public posts
- **Description**: With this method you can only change the Title, Content, Status and Category. By changing the `status` you can also encrypt the posts. If the post is encrypted you might want to look into [Updating encrypted posts](#updating-encrypted-posts)
- **Endpoint**: `/posts/<serial>`
- **Method**: PUT
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
404: {"message": "There is no post with this serial. Please recheck."}
500: {"message": "There was an error with the encryption. Try again."}
500: {"message":"Something went wrong. We can't upload this in our database."}
```
### Updating encrypted posts
- **Description**: With this method you can only change the Title, Content, Status and Category. By changing the `status` you can also decrypt the posts. If the post is not encrypted you might want to look into [Updating public posts](#updating-public-posts)
- **Endpoint**: `/posts/<serial>/<key>`
- **Method**: PUT
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
404: {"message": "There is no post with this serial. Please recheck."}
500: {"message":"Something went wrong. We can't upload this in our database."}
```

# Articles
- [List of HTTP status codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes)
