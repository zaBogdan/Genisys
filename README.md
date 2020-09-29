# Genisys - Backend API

This is the core of my website backend. It will handle Authorization, CRUD operations, Mailing, Logging and much more. This is written in Python3 using as main framework Flask. 

### Instalation with docker
Because it was a bit of a stretch to install on all my devices this project I've decided to use docker containerization and I've ended up reducing the steps and adding more redundancy

1. Clone this repository using: `git clone https://github.com/zaBogdan/Genisys.git`
2. Complete `.env.example` with the credentials and rename it to `.env` 
3. Fire up a terminal, type `cd Genisys` and use `docker-compose up --build`
4. And that's it. Now you can acess it using `http://localhost:1337`

Please note that `--build` tag must be used only at first run, not everytime. 

### Instalation without docker
The hole projected was coded on a NIX based system, macOS to be specific, but it can be run on each an every system which has [python](https://www.python.org/) and [pipenv](https://pypi.org/project/pipenv/) installed. It's also using a **MySQL** database so you must have one installed on the machine or over the network. 

1. Clone this repository using: `git clone https://github.com/zaBogdan/Genisys.git`
2. Fire up a console, go to the directory and type `pipenv install`
3. From now you will use `pipenv shell` to have the virtual environment of python
4. To run the app just use `python app.py`

> Note: Before you run the app you need to setup the `.env` file, which should be in the root folder. You have a file called `.env.example` for that.

### Endpoints
I decided not to oversize this file and I created a new one with all endpoints of this API documented and with examples. All the reponses from each call can be found in here to. For further more you can look [here](Endpoints.md).

> Note: Here you can found only the working endpoints that have been tested and are 100% functional. For the **others**, which are in development or to be done, check down in this file, at [Developing](#developing). 

### Improvements
This needs to be done before of the releasing date, which is not yet known. It's a high change to be around the 1'st May. 
- [x] Add the option for posts to be encrypted
- [x] Add the option for posts to be decrypted. 
- [x] Link the posts with the author, by adding foreignKeys
- [ ] Find a way to store for 30 days the deleted posts. 
- [x] Secure the API
- [ ] Logout functionality
- [ ] Add some role system
- [ ] Add activity feature (using the access & refresh tokens)
- [x] Add a monitoring system and be able to recieve it (Logger implementation)

### Developing
None of the following can be used in a production enviroment. Some are full of bugs or not yet started. For the working ones you can check [Endpoints Docs](Endpoints.md)

1. Posts
    - Delete a post by its id
2. Authors
    - Logout an user, revoking it's credentials.
3. Mailing 
    - Be able to send mails to users
    - Send email if something critical occurs.
