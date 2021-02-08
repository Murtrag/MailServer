# MailServer

## Install
1. Pull project:
```
git pull https://github.com/Murtrag/MailServer.git
```
2. Go to project directory:
```
cd MailServer
```
3. Run containers:
```
$ docker-compose -f docker-compose.yaml up -d
```
4. Go to app container:
```
docker exec -it mailserver_app bash
```
5. Run setup file:
```
# python3 setup.py
```

## Usage
### Users
'''
./main.py -u user -p password
'''

Creates a new user.

'''
./main.py -u user -p password -e -n new_password
'''

Changes user's password

'''
./main.py -u user -p password -d
'''

Deletes user from database.

### Messages
'''
./message.py -u login -p password -l
'''

Displays all user's messages

'''
./message.py -u login -p password -t another_user@domain.com -s 'topic::message to send'
'''

Sends message to another user

## Development Tips
Run tests:
'''
# python3 -m pytest
'''

Tests should be run inside of the container because of the connection with the db
marks:
- connection
- user
- messages
- clcrypto
