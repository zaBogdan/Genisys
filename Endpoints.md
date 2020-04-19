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
This category handles all the thing related to reading/creating/updating/deleting content from the database. The methods support AES encryption.

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
200: "data": <JSON Object>
400: "This is an encrypted post. To read it's content you must pass the encryption key" (Bad request)
404: "There is no post with this serial. Please recheck." (Not found)
```
### Encrypted posts
- **Description**: You can read encrypted posts by it's serial attribute, look up at the [serial definition](#reading-by-serial). You need to pass the original encryption key to decode it.
- **Endpoint**: `/post/<serial>/<key>`
- **Method**: GET
- **Body**: None
- **Reponses**:
```json
200: "data": <JSON Object>
400: "This post is not encrypted. Everyone can read it." (Bad request.)
401: "That's the wrong key. We can't decrypt the message." (Unauthorized)
404: "There is no post with this serial. Please recheck." (Not found)
```

## Dumping posts
With the help of this endpoint you can dump the whole posts from the database, or you can add filters. 

