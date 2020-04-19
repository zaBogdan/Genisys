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
        -[Updating public posts](#updating-public-posts)
        -[Updating encrypted posts](#updating-encrypted-posts)

# Posts
This category handles all the thing related to reading/creating/updating/deleting content from the database. The methods support AES encryption. All of the requests take in and reponde with **JSON** data. 

## Reading by serial
Here I will define the serial termen, and others if is needed.
`serial` is a way of indexing data, wich can handle up to 36 at 8th power different variables. It can only contain lower ascii letters (a-z) and all digits(0-9). This can not be changed anytime, so it's bound to the post (it doesn't matter that the title or author changes) all the time.

### Public posts
- **Description**: You can read posts by it's serial attribute, look up at the [serial definition](#reading-by-serial). You will retrieve only one post from this method and it must not have the status 'encrypted'.  
- **Endpoint**: `/post/<serial>`
- **Method**: GET
- **Body**: None
- **Reponses**:
```json
200: {"data": <JSON Object>}
400: {"message": "This is an encrypted post. To read it's content you must pass the encryption key"} (Bad request)
404: {"message": "There is no post with this serial. Please recheck."} (Not found)
```
### Encrypted posts
- **Description**: You can read encrypted posts by it's serial attribute, look up at the [serial definition](#reading-by-serial). You need to pass the original encryption key to decode it.
- **Endpoint**: `/post/<serial>/<key>`
- **Method**: GET
- **Body**: None
- **Reponses**:
```json
200: "data": <JSON Object>
400: {"message": "This post is not encrypted. Everyone can read it."} (Bad request.)
401: {"message": "That's the wrong key. We can't decrypt the message."} (Unauthorized)
404: {"message": "There is no post with this serial. Please recheck."} (Not found)
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
```json
200: 
{
"count" : <int>,
"data": <JSON Object>
}
404: {"message": "There are no posts yet."} (Not found)
```

### Dumping by Author
- **Description**: You can dump all the posts from the same author. They are sorted by the last created at the time of request. 
- **Endpoint**: `/posts/author/<name>`
- **Method**: GET
- **Body**: None
- **Reponses**:
```json
200: 
{
"count" : <int>,
"data": <JSON Object>
}
404: {"message": "This author didn't posted yet."} (Not found)
```

### Dumping by Category
- **Description**: You can dump all the posts from the same category. They are sorted by the last created at the time of request. 
- **Endpoint**: `/posts/category/<name>`
- **Method**: GET
- **Body**: None
- **Reponses**:
```json
200: 
{
"count" : <int>,
"data": <JSON Object>
}
404: {"message": "There are no posts in this category yet."} (Not found)
```

## Creating
With this endpoint, you can add different posts in our database. 
> Note: If you want to encrypt a post from this stage, setting the `encryptionKey` will be enough. The status will be overwritten by default to `encrypted` when you have that parameter.  

- **Endpoint**: `/post`
- **Method**: POST
- **Body**: 
```JSON
{
	"author": "",
	"status": "",
	"category": "",
	"content": "",
	"title": "",
	"encryptionKey": ""
}
```
> Note: `encryptionKey` is optional and it's only for encryption (obviously...). You can just ignore it if you make a `public` post. 
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
	"status": "",
	"category": "",
	"title": "",
	"content": ""
}
```
And this is how you encrypt a public post with this method. Parameter `encryptionKey` is a must and it can be empty. Without him it will throw an error. Note that you can only pass `status` and `encryptionKey` to do the encryption. 
```JSON
{
	"status": "encrypted",
	"category": "",
	"title": "",
	"content": "",
	"encryptionKey": ""
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
	"title": "",
	"content": "",
	"category": ""
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
