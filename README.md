# Gitlab projects parser API 

#### Find all Gitlab projects with name/description consisting of a search query

Framework: Django REST

Database: SQLite3

## Usage

Running inside Docker container (in the background): `docker-compose up -d`

Or running by terminal commands: `python -m venv env`, 
`pip install -r requirements.txt`, `python manage.py migrate`, 
`python manage.py runserver`

Testing by command: `python manage.py test`

Admin panel: `localhost:8000/admin` 
(creating admin by command: `python manage.py createsuperuser`)

API: `localhost:8000/api`

Single API instance: `localhost:8000/api/<identifier>`

## Requests
- **POST /api** 

Arguments: 

- Search query: any character string

Response: `201 Created` on success

All responses will have the form
```json
{
    "id": "auto defined by database",
    "search_query": " string defined by user input",
    "gitlab_data": [
        {
            "id": "project ID",
            "name": "project name",
            "description": "project description",
            "last_activity_at": "last project update datetime"
        },
    ],
    "created_at": "query creation datetime"
}
```

Response: `400 Bad Request` if projects are not exist 

```json
{
    "error": "There are no projects for this search query"
}
```

- **GET /api** or **GET /api/<identifier<identifier>>**

Response: `200 OK` on success

Example of response `GET /api/1`
```json
{
    "id": 1,
    "search_query": "kremlin",
    "gitlab_data": [
        {
            "id": 12493512,
            "name": "kremlin",
            "description": "Kevin's gremlin cli tool. Since we can't run attacks on remote machines, wrote this to do so.",
            "last_activity_at": "2019-05-28T02:37:09.398000+03:00"
        },
        {
            "id": 10828930,
            "name": "thekremlin",
            "description": "",
            "last_activity_at": "2019-02-13T19:29:48.578000+03:00"
        }
    ],
    "created_at": "2020-03-15T20:50:20.421920+03:00"
}
```

Response: `404 Not found` if a search query does not exist

```json
{
    "detail": "Not found."
}
```
- **DELETE /api/<identifier<identifier>>**

Response: `400 No Content` on success

Response: `404 Not found` if a search query does not exist
