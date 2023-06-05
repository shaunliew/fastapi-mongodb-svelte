# fastAPI and MongoDB

## How to run the FastAPI backend (in Linux)

note: make sure you install 

[python version 3.10](https://docs.python-guide.org/starting/install3/linux/)

[mongoDB](https://www.mongodb.com/docs/manual/administration/install-on-linux/)

[mongoDB Compass](https://www.mongodb.com/docs/compass/current/install/)
### For MongoDB

1. start your mongoDB server
```
sudo service mongod start
```

1. check whteher mongoDB server is activated
```
mongosh
```

### For fastAPI
1. create a virtual env
```
python -m venv venv
```

2. install all the necessary packages
```
pip install -r requirements.txt
```

3. Start the fastAPI
```
uvicorn app:app --reload   
```

### reference
[Getting Started with MongoDB and FastAPI](https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/)

[Problem of MongoDB connect econnrefused 127.0.0.127017](https://stackoverflow.com/questions/50173080/mongonetworkerror-failed-to-connect-to-server-localhost27017-on-first-connec)