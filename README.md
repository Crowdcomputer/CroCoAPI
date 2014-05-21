# CroCo API


Building the future of Crowdsourcing API: crowdsourcing as a service

## API Documentation

### Authentication
The APIs are build with *token* authentication.
In order to retrive your token, you have to:
- create the user: **User are created manually for the time being.**
- `POST` to `api-token-auth/` passing `username` and `password`

EXAMPLE:
```
curl -H "Content-Type: application/json" -d '{"username":"Stefano","password":"stefano"}' localhost:8000/api-token-auth/

{"token": "8babeaea2a837621327606970f0f16c7c4fbf0d8"}
```

token must be used in the header of ALL the other calls, using  `Authorization: Token <Your Token>`

###TASK
Task api allows one to:
- See the list of all his tasks
- Create/Read/Update/Delete (CRUD) a task
- Start/Stop a task 
- See the list of all the instances of a task
- Create/Read/Update/Delete (CRUD) a taskInstance
- Assign a taskInstance to a User
- Update the results of a taskIntance (execute the instance) 

####List
`GET` to `task/`
```
curl -H "Authorization: Token 8babeaea2a837621327606970f0f16c7c4fbf0d8"  localhost:8000/task/


[{"owner": "stefano", "id": 1, "title": "edited", "description": "descaaa", "date_created": "14:34:21.701", "date_deadline": "2014-05-05T12:00:00Z", "status": "ST", "uuid": "52ed354a896a4ca38edd3946d58d7b06", "page_url": "http://example.com"}, {"owner": "stefano", "id": 3, "title": "2", "description": "2", "date_created": "20:08:40.446", "date_deadline": "2014-05-05T12:00:00Z", "status": "ST", "uuid": "", "page_url": "http://test.com"}
```

####CREATE
To **Create** `POST` to `task/` with following parameters:
- `title`: the title of the task
- `description`: the description of the task, what a worker has to do
- `date_deadline`: when the task expires (format: `YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HHMM|-HHMM|Z]`)
- `page_url`: the page that implements the task UI 

```
curl -H "Content-Type: application/json" -H "Authorization: Token 8babeaea2a837621327606970f0f16c7c4fbf0d8" -d '{"title":"title","description":"desc","date_deadline":"2014-06-06T12:00","page_url":"http://www.crowdcomputer.org"}' localhost:8000/task/


{"owner": "stefano", "id": 4, "title": "title", "description": "desc", "date_created": "14:34:34.331", "date_deadline": "2014-06-06T12:00:00", "status": "ST", "uuid": "", "page_url": "http://www.crowdcomputer.org"}
```
####READ
To **Read** `GET` to `task/<ID>/`
####UPDATE
To **Update** `PUT` to `task/<ID>/` with paramters as the creation
####DELETE
TO **Delete** `DELETE` to `task/<ID>/`

####START
To **Start** `POST` to `task/<ID>/start/`
####STOP
To **Stop** `POST` to `task/<ID>/stop/`

####LIST OF INSTANCES
To **get the list** `GET` to `task/<ID>/intance/`

####CREATE INSTANCE
To **Create** `POST` to `task/<ID>/instance/` with following parameters:
- `input`: the JSON that is the input of the instance

```
curl -H "Content-Type: application/json" -H "Authorization: Token 8babeaea2a837621327606970f0f16c7c4fbf0d8" -d '{"input":{"title":"title","description":"desc","date_deadline":"2014-06-06T12:00","page_url":"http://www.crowdcomputer.org"}}' localhost:8000/task/1/instance/

{"executor": null, "task": "edited", "owner": "stefano", "input_data": {"page_url": "http://www.crowdcomputer.org", "description": "desc", "date_deadline": "2014-06-06T12:00", "title": "title"}, "output_data": null, "id": 24, "status": "ST", "date_created": "2014-05-21T15:05:09.209Z", "date_started": null, "date_finished": null, "uuid": "3523f417c4994650b2865279febd079a", "parameters": "{}"}
```
####READ INSTANCE
To **Read** `GET` to `task/<ID_TASK>/instance/<ID>/`
####UPDATE INSTANCE
To **Update** `PUT` to `task/<ID_TASK>/instance/<ID>/` with paramters as the creation
####DELETE INSTANCE
TO **Delete** `DELETE` to `task/<ID_TASK>/instance/<ID>/`

####START INSTANCE
To **Start** `POST` to `task/<ID_TASK>/instance/<ID>/start/`
####STOP INSTANCE
To **Stop** `POST` to `task/<ID_TASK>/instance/<ID>/stop/`
####ASSIGN INSTANCE
To **assign a user to an instance** `POST` to `task/<ID_TASK>/instance/<ID>/assign/` with following parameters: 
- `worker`: the `id` of the worker

```
curl -H "Content-Type: application/json" -H "Authorization: Token 8babeaea2a837621327606970f0f16c7c4fbf0d8" -d '{"worker":1}' localhost:8000/task/1/instance/1/assign/

{"executor": "stefano", "task": "123", "owner": "b", "input_data": null, "output_data": null, "id": 1, "status": "ST", "date_created": "2014-05-05T16:13:33.782Z", "date_started": null, "date_finished": null, "uuid": "1312321312", "parameters": "{}"}
```
**executor** is assigned
####EXECUTE INSTANCE
To **store the results of an instance** `POST` to `task/<ID_TASK>/instance/<ID>/execute/`  with following parameters: 
- `restult`: the json of the result data

```
curl -H "Content-Type: application/json" -H "Authorization: Token 8babeaea2a837621327606970f0f16c7c4fbf0d8" -d '{"result":{"v1":"this is the result"}}' localhost:8000/task/1/instance/1/execute/

{"executor": "stefano", "task": "123", "owner": "b", "input_data": null, "output_data": {"v1": "this is the result"}, "id": 1, "status": "ST", "date_created": "2014-05-05T16:13:33.782Z", "date_started": null, "date_finished": null, "uuid": "1312321312", "parameters": "\"\\\"\\\"\""}

