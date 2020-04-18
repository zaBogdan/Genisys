# zaBogdan - Backend API

### Endpoints
Posts ( All are GET Requests)
```
/posts/category/<name> #All posts from a specific category
/posts/author/<name> #All posts created by an author
/posts #All post from the database with public status
```

Post
```
GET /post/<id> #Get a post by serial id
PUT /post/<id> #Update a pust by id
DELETE /post/<id> #Delete a post by its id
POST /post #Create a new post
```

Authors (TBD)
```
GET /author/<name> #Information about specific author & his posts
POST /author/<name> #Create a new author
PUT /author/<name> #Update author information
DELETE /author/<name> #Delete an existing author
```

> All so called `Deletes` will be moved in `Archived` Database, with specific encryption

### Improvements
Here is a list of to be done before release:
- [x] Add the option of posts to be encrypted
- [ ] Add the option for posts to be decrypted. 
- [ ] Link the posts with the author, by adding foreignKeys
- [ ] Found a way to store for 30 days the deleted posts. 