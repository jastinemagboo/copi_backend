## Backend Architecture

The backend of this application is built using Flask, SQLAlchemy, and PostgreSQL. Below is an overview of the backend structure and the main components.

### 1. `app.py`

This is the main entry point of the application.

**Flask app creation**: The `create_app()` function is used to create and configure the Flask app. It loads configuration settings from the `Config` class in `config.py`.

**Database initialization**: The `db.init_app(app)` is used to bind the Flask app with SQLAlchemy, which enables the app to interact with the PostgreSQL database.

**Blueprint registration**: The `post_bp` blueprint from `routes.post_routes` is registered with the Flask app. Blueprints are used to organize routes in a modular way, making the app more maintainable.

**Key Routes**: The app will load routes from the `post_routes` blueprint.

### 2. `config.py`

This file contains configuration settings for the application.

**SQLAlchemy URI**: The `SQLALCHEMY_DATABASE_URI` is set to the PostgreSQL database URL. This is where SQLAlchemy will connect to store and retrieve data. It can be updated to use an environment variable `DATABASE_URL` for different environments.
**Disabling modification tracking**: The `SQLALCHEMY_TRACK_MODIFICATIONS` is set to `False` to prevent Flask from tracking modifications of objects and to save memory.

### 3. `extensions.py`

This file initializes the database extension (`SQLAlchemy`) for the app.

**SQLAlchemy instance**: The `db` object is created using `SQLAlchemy()`. This object is then imported and used in other files (such as `models/post_model.py` and `routes/post_routes.py`) to interact with the database.
**Initialization**: `db.init_app(app)` is called in `app.py` to bind the database extension to the Flask app.

### 4. `models/post_model.py`

The `Post` model defines the structure of the posts table in PostgreSQL.

- **Post table**: The table `copi_posts` is defined using SQLAlchemy's ORM. It has the following columns:
  - `id`: A UUID column that serves as the primary key for each post.
  - `title`: A string column to store the title of the post.
  - `content`: A text column to store the content of the post.
  - `created_at`: A datetime column that is automatically set to the current timestamp when the post is created.
  - `updated_at`: A datetime column to store when the post was last updated.
  - `deleted_at`: A datetime column that is used for soft deletes (when a post is deleted but not permanently removed).

### 5. `routes/post_routes.py`

This file contains the routes for managing posts, and it is registered as a blueprint in `app.py`.

**Create Post** (`POST /posts`):

- This route allows the creation of a new post. It expects a JSON body with `title` and `content`. If these fields are missing, it returns an error response.
- Once the post is created, it is saved to the database, and a success message along with the post data is returned.

**Get Posts** (`GET /posts`):

- This route retrieves all posts that have not been marked as deleted (i.e., their `deleted_at` field is `None`). The posts are ordered by their `created_at` timestamp in descending order.
- The response contains a list of all posts, including their `id`, `title`, `content`, `created_at`, and `updated_at`.

**Update Post** (`PATCH /posts/<uuid:id>`):

- This route allows updating the title and/or content of a post. If neither `title` nor `content` is provided, a 400 error is returned.
- Once updated, the `updated_at` field is set to the current datetime.

**Delete Post** (`DELETE /posts/<uuid:id>`):

- This route marks a post as deleted by setting the `deleted_at` field to the current datetime. This is a "soft delete" approach, meaning the post remains in the database but is considered deleted.
- If the post is not found, a 404 error message is returned.

### 6. Database Operations and Soft Deletion

- **Database Session**: SQLAlchemy uses a session (`db.session`) to handle database operations. Each operation, like adding, committing, or deleting data, happens within a session.
- **Soft Deletion**: When a post is "deleted," its `deleted_at` field is updated with the current timestamp. This allows the post to remain in the database but be excluded from regular queries (such as in the `GET /posts` route). This is a soft delete approach, which is often preferred in applications where data recovery might be needed.

### 7. Running the Application

To run the app locally, simply execute the following command:

**Using Bash**

- git clone <repository-url>
- python -m venv venv
- source venv/Scripts/activate
- pip install -r requirements.txt
- pip install flask
- Create .env and Add necessary environment variables.
  Database URL Format - (DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>)
- python app.py
