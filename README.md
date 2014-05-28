
FORMAT: 1A
# CrowdComputer (CroCo) API
This is the ***Crowdcomputer API***. This API provides and easy way to crowdsourcer your application.
Building the future of Crowdsourcing API: crowdsourcing as a service

[Crowdcomputer](www.crowdcomputer.org) is created at the University of Trento, Italy by [Stefano](www.stefanotranquillini.me) and [Pavel](www.kucherbaev.com).

#Group Task
## Task [/task/]

### Retrive the list of task [GET]
This method returns the list of tasks that are created by that specific application

+ Request (text/plain)
    + Headers

            Authorization: Token 1

+ Response 201 (application/json)

    + Body

            [
                {
                    "owner": "stefano", 
                    "id": 1, 
                    "title": "Task 1", 
                    "description": "Desc Task 1", 
                    "date_created": "2014-05-01T14:34:21.701", 
                    "date_deadline": "2014-05-05T12:00:00Z", 
                    "status": "ST", 
                    "uuid": "52ed354a896a4ca38edd3946d58d7b06", 
                    "page_url": "http://www.crowdcomputer.com/testpage.html",
                    "reward" : 1.0
                }, 
                {
                    "owner": "stefano", 
                    "id": 3, 
                    "title": "Task 2",
                    "description": "task 2", 
                    "date_created": "2014-05-01T20:08:40.446", 
                    "date_deadline": "2014-05-05T12:00:00Z", 
                    "status": "ST", 
                    "uuid": "df78d71867de49029163aca10bf534de", 
                    "page_url": "http://www.crowdcomputer.com/testpage.html",
                    "reward" : 1.0
                }
            ]

### Create a task [POST]
This creates a task. ***Page URL*** must be an external webpage prepared following the instructions (NOT YET ONLINE). ***reward*** has to be specified in EUR.

+ Request JSON message
    + Headers

            Authorization:Token 1

    + Body
        
            {
                "title" : "Task title",
                "description" : "Task Description",
                "date_deadline" : "2014-05-05T12:00:00Z",
                "page_url":"http://www.crowdcomputer.org/testme.html",
                "reward": 0.5
            }

+ Response 201 (application/json)

    + Body

            {
                "owner": "stefano", 
                "id": 4, 
                "title": "Task title",
                "description": "Task Description", 
                "date_created": "2014-05-02T21:08:40.446", 
                "date_deadline": "2014-05-05T12:00:00Z", 
                "status": "ST", 
                "uuid": "feed552cd3174a49a4d1324e2cc53de8", 
                "page_url": "http://www.crowdcomputer.com/testme.html",
                "reward" : 0.5
            }

## Task Detail [/task/{id}/]

+ Parameters
    
    + id (required, number) ... The id of the task.

### Get a task [GET]
This updates a task.

+ Request JSON message
    + Headers

            Authorization:Token 1

    + Body
        
+ Response 200 (application/json)

    + Body

            {
                "owner": "stefano", 
                "id": 4, 
                "title": "Task title edited",
                "description": "Task Description", 
                "date_created": "2014-05-02T21:08:40.446", 
                "date_deadline": "2014-05-05T12:00:00Z", 
                "status": "ST", 
                "uuid": "feed552cd3174a49a4d1324e2cc53de8", 
                "page_url": "http://www.crowdcomputer.com/testme.html",
                "reward" : 0.5
            }


### Update a task [PUT]
This updates a task.

+ Request JSON message
    + Headers

            Authorization:Token 1

    + Body
        
            {
                "title" : "Task title edited",
                "description" : "Task Description",
                "date_deadline" : "2014-05-05T12:00:00Z",
                "page_url":"http://www.crowdcomputer.org/testme.html",
                "reward": 0.5
            }

+ Response 200 (application/json)

    + Body

            {
                "owner": "stefano", 
                "id": 4, 
                "title": "Task title edited",
                "description": "Task Description", 
                "date_created": "2014-05-02T21:08:40.446", 
                "date_deadline": "2014-05-05T12:00:00Z", 
                "status": "ST", 
                "uuid": "feed552cd3174a49a4d1324e2cc53de8", 
                "page_url": "http://www.crowdcomputer.com/testme.html",
                "reward" : 0.5
            }

### Delete a task [DELETE]
This delete a task.

+ Request (*/*)
    + Headers

            Authorization:Token 1

    + Body
        
+ Response 204 (application/json)

    + Body

## Start a task [/task/{id}/start/] 
This starts a task

+ Parameters
    
    + id (required, number) ... The id of the task.

### Start [PUT]

+ Request (*/*)
    + Headers

            Authorization:Token 1

    + Body
        
+ Response 200 (application/json)

    + Body

            {
                'status':'PR'
            }  

## Stop a task [/task/{id}/stop/] 
This stops a task

+ Parameters
    
    + id (required, number) ... The id of the task.

### Stop [PUT]

+ Request (*/*)
    + Headers

            Authorization:Token 1

    + Body
        
+ Response 200 (application/json)

    + Body

            {
                'status':'ST'
            }  


#Group TaskInstance
## Task [/task/{id}/taskinstance]

+ Parameters
    
    + id (required, number) ... The id of the task.

### Retrive the list of taskinstance of a task [GET]
This method returns the list of the task instances of the task identified with `id`

+ Request (text/plain)
    + Headers

            Authorization: Token 1

+ Response 201 (application/json)

    + Body

            [
               ...
            ]

### Create a taskInstance [POST]
This creates a task instance. ***input*** is the input data for that specific instnace.
This functions checks if the balamnce of the workers is enough to pay this instance.

+ Request JSON message
    + Headers

            Authorization:Token 1

    + Body
        
            {
                "input" : {} //optional, must be a json
            }

+ Response 201 (application/json)

    + Body

            {
                ...
            }

## TaskInstance Detail [/task/{id}/taskinstance/{id_instance}/]

+ Parameters
    
    + id (required, number) ... The id of the task.
    + id_instance (required, number) ... The id of the task instance.

### Get a task instnace [GET]
This returns the details of  a task instance.

+ Request JSON message
    + Headers

            Authorization:Token 1

    + Body
        
+ Response 200 (application/json)

    + Body

            {
            ...
            }

### Update a task instance [PUT]
This updates a task instance.

+ Request JSON message
    + Headers

            Authorization:Token 1

    + Body
        
            {
              ...
            }

+ Response 200 (application/json)

    + Body

            {
               ...
            }

### Delete a task instance [DELETE]
This delete a task.

+ Request (*/*)
    + Headers

            Authorization:Token 1

    + Body
        
+ Response 204 (application/json)

    + Body

## Start a task instance [/task/{id}/taskinstance/{id_instance}/start/] 
This starts a task

+ Parameters
    
    + id (required, number) ... The id of the task.
    + id_instance (required, number) ... The id of the task instance.


### Start [POST]

+ Request (*/*)
    + Headers

            Authorization:Token 1

    + Body
        
+ Response 200 (application/json)

    + Body

            {
                'status':'PR'
            }  

## Stop a task instance [/task/{id}/taskinstance/{id_instance}/stop/] 
This stops a task

+ Parameters
    
    + id (required, number) ... The id of the task.
    + id_instance (required, number) ... The id of the task instance.


### Stop [POST]

+ Request (*/*)
    + Headers

            Authorization:Token 1

    + Body
        
+ Response 200 (application/json)

    + Body

            {
                'status':'ST'
            }  

## Assign a task instance to a worker [/task/{id}/taskinstance/{id_instance}/assign/] 
This assign the task instance to a worker

+ Parameters
    
    + id (required, number) ... The id of the task.
    + id_instance (required, number) ... The id of the task instance.


### Assign [POST]

+ Request (*/*)
    + Headers

            Authorization:Token 1

    + Body
    
            {
                'worker': 1 //id of the worker

            }
        
+ Response 200 (application/json)

    + Body

            {
               ...
            }  

## Execute a task instance, thus update the task instance metadata [/task/{id}/taskinstance/{id_instance}/execute/] 
This updates the task instance metadata.

+ Parameters
    
    + id (required, number) ... The id of the task.
    + id_instance (required, number) ... The id of the task instance.


### Assign [POST]

+ Request (*/*)
    + Headers

            Authorization:Token 1

    + Body

            {
                'result': {} //a json object

            }
        
+ Response 200 (application/json)

    + Body

            {
               ...
            }  



