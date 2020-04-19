# Endpoints documentation
1. [Posts](#posts)
    - [Reading by serial](#reading-by-serial)
        - [Reading public posts](#reading-public-posts)
        - [Reading encrypted posts](#reading-encrypted-posts)
    - [Dumping posts](#dumping-posts)
        - [Dump all](#dump-all)
        - [Dumping by author](#dumping-by-author)
        - [Dumping by category](#dumping-by-category)
    - [Creating](#creating)
    - [Updating](#updating)
        -[Updating public posts](#updating-public-posts)
        -[Updating encrypted posts](#updating-encrypted-posts)

# Posts
This category handles all thing related to reading/creating/updating/deleting content from the database. The methos support AES encryption.

### Reading public posts
Description: `Read a post using the serial. Note: It's status should not be encrypted.`
Endpoint: `/post/<serial>`
Method: `GET`
Data: `None`
Reponses:
```JSON
200: "data": <JSON Object>
400: This is an encrypted post. To read it's content you must pass the encryption key (Bad request. The post is encrypted.)
404: "There is no post with this serial. Please recheck." (Not found)
```

### Reading encrypted posts by serial
Description: `Read an encrypted post by passing it's serial and encryption key.`
Endpoint: `/post/<serial>/<encryptionKey>`
Method: `GET`
Data: `None`
Reponses: 
```
200: "data": <JSON Object>
400: "This post is not encrypted. Everyone can read it." (Bad requst. The post is not encrypted.)
401: "That's the wrong key. We can't decrypt the message."(Unauthorized. The encryption key doesn't match to the original one.)
404: "There is no post with this serial. Please recheck." (Not found)
```

_Model_
Description: ``
Endpoint: ``
Method: ``
Data: 
```
```
Reponses: 
```
```