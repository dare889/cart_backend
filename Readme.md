## Flask Migrate Commands

```    
    $env:FLASK_APP="app.py"
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
```

### Flask Migrate Commands Add products table
```
    $env:FLASK_APP="app.py"
    flask db migrate -m "Add products table"
    flask db upgrade
```

### Flask Migrate Commands Add orders table
```
    $env:FLASK_APP="app.py"
    flask db migrate -m "Add orders table"
    flask db upgrade
```

# Run migrations Update
```
    flask db init
    flask db migrate -m "Update Product model"
    flask db upgrade
```

### Install

```
    pip install -r requirements.txt
```

### Run

```
    flask run
```

## Docker

```
    docker build -t flask-api .
    docker run -p 5000:5000 flask-api
```

### Docker Compose

```
    docker-compose up
```

### Docker Compose Down

```
    docker-compose down
```

### Docker Compose Build

```
    docker-compose up --build
```

### Docker Compose Down and Remove Volumes

```
    docker-compose down -v
```

### Access the API

```
    http://localhost:5000
```

### Register a new user with test data with test json in postman

```
    http://localhost:5000/register
    {
        "username": "test",
        "email": "test@test.com",
        "password": "test"
    }
```
