## DRF Generic Views for Book CRUD

This project exposes read and write endpoints for the `Book` model using Django REST Framework generic views.

### Endpoints
- `GET /api/books/` — list all books (public)
- `GET /api/books/<pk>/` — retrieve a book (public)
- `POST /api/books/create/` — create a book (authenticated)
- `PATCH /api/books/<pk>/update/` — update a book (authenticated)
- `DELETE /api/books/<pk>/delete/` — delete a book (authenticated)

### Permissions
- Read endpoints (`list`, `retrieve`): `AllowAny`
- Write endpoints (`create`, `update`, `destroy`): `IsAuthenticated`

### Validation
`BookSerializer` validates that `publication_year` is not in the future. Requests with a future year are rejected with a 400 response.

### Quickstart
1) Install dependencies and run migrations:
```bash
. .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

2) Create a user for authenticated requests:
```bash
python manage.py createsuperuser --username apiuser --email test@example.com
# set password when prompted (e.g., apipass123)
```

3) Run the dev server:
```bash
python manage.py runserver
```

4) Test with curl:
```bash
# List (public)
curl -s http://127.0.0.1:8000/api/books/

# Create (authenticated)
curl -s -u apiuser:apipass123 \
  -H 'Content-Type: application/json' \
  -d '{"title":"API Book","publication_year":2020,"author":1}' \
  http://127.0.0.1:8000/api/books/create/

# Update (authenticated)
curl -s -u apiuser:apipass123 -X PATCH \
  -H 'Content-Type: application/json' \
  -d '{"title":"API Book Updated"}' \
  http://127.0.0.1:8000/api/books/1/update/

# Delete (authenticated)
curl -s -u apiuser:apipass123 -X DELETE \
  http://127.0.0.1:8000/api/books/1/delete/
```

### Notes
- The nested relationship between `Author` and `Book` is handled via the `AuthorSerializer` which includes a nested, read-only list of `Book` entries.
- Views live in `api/views.py`, routes in `api/urls.py`, and are included at `advanced_api_project/urls.py` under the `/api/` prefix.


