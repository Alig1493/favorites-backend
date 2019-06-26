Favorite Things Backend
======
*A backend app to help keep track of your favorite things!*

## Disclaimer
This project has been built by using our custom [cookie-cutter](https://github.com/mashrikt/cookiecutter-django-dokku)
project that was built overtime in our careers. This is still a work in 
progress and having used this might mean there are a few extra 
libraries and functionality that are present but unused in this project.
I chose to use this cookie cutter for rapid development and deployment 
purposes.

Also would prefer to use [djang-dirty-fields](https://github.com/romgar/django-dirtyfields)
to track my model field changes, since my applied `ModelDiffMixin` might 
not cover most cases of state changes.

## Database Entity Relationship of models
![Favorite Things ER](favorite_things.png?raw=true "Favorite things ER")

* A user can have many different favorite things
* One category can have multiple favorite things
* One favorite thing can have one category
* Only showing the PK and FK labels
* Used built in admin log entry models to save audit log
changes. I took this approach because I thought it better to use
something django already provides. This will also allow us
to query for changes on a specific date. The change message stores
the favorite field value model object changes.
* Log(audit_log) only shows the latest changes

(P.S: I think it might have been better to create another 
model based off of the LogEntry model for logging our model
changes and not having conflicts since changes made by the admin
panel are also being save in our currently used log entry model.)

### Deployment
* Deployed using [dokku](http://dokku.viewdocs.io/dokku/)
* Added ssl using dokku built in methods since our front end
that was deployed using netlify and it enabled ssl over there.
As a result we had to add a certificate in order to consume our backend 
resources
* Deployed link: https://13.235.4.179/
* Login credentials:
    * username: admin
    * password: admin12345
* Opening the deployed link will give you a warning since 
the ssl was added but it wasn't verified using a custom CNAME 
domain.

### Example requests and responses
``POST http://0.0.0.0:8000/api/v1/favorites/``

``request data``
```json
{
    "category": "food",
    "title": "burger",
    "ranking": 1,
    "metadata": null,
    "description": ""
}
```

``response``
```json
{
    "id": 1,
    "logs": [],
    "category": "food",
    "created_date": "2019-06-26",
    "modified_date": "2019-06-26",
    "title": "burger",
    "ranking": 1,
    "metadata": null,
    "description": ""
}
```

``PUT http://0.0.0.0:8000/api/v1/favorites/1/``

``request data``
```json
{
    "category": "food",
    "title": "pizza",
    "ranking": 1,
    "metadata": null,
    "description": ""
}
```

``response``
```json
{
    "id": 1,
    "logs": [
       "{'title': ('burger', 'pizza')}"
    ],
    "category": "food",
    "created_date": "2019-06-26",
    "modified_date": "2019-06-26",
    "title": "burger",
    "ranking": 1,
    "metadata": null,
    "description": ""
}
```

``GET http://0.0.0.0:8000/api/v1/favorites/``

``response``
```json

[
  {
    "id": 1,
    "title": "person",
    "favorite_things": []
  },
  {
    "id": 2,
    "title": "place",
    "favorite_things": [
      {
        "id": 2,
        "logs": [
            "{'title': ('bangkok', 'tokyo')}"
        ],
        "category": "place",
        "created_date": "2019-06-26",
        "modified_date": "2019-06-26",
        "title": "tokyo",
        "ranking": 1,
        "metadata": null,
        "description": ""
      }
    ]
  }
]
```

``GET http://0.0.0.0:8000/api/v1/favorites/1/``

``response``
```json
{
    "id": 1,
    "logs": [
        "{'title': ('burger', 'pizza')}"
    ],
    "category": "food",
    "created_date": "2019-06-26",
    "modified_date": "2019-06-26",
    "title": "pizza",
    "ranking": 1,
    "metadata": null,
    "description": ""
}
```

DOCUMENTATION: https://13.235.4.179/docs/

## Docker compose commands to run project:
Make sure you have docker and docker compose installed
`docker-compose up --build`

Pytest:
* Log into docker compose shell via exec: `docker-compose exec web bash`
* Run this command in shell: `pytest`