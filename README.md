# Song Recommendation API

A production-oriented backend for a personalized song recommendation system built with Django REST Framework, PostgreSQL, Redis, Celery, and Docker.

The application provides user preference management, Spotify-based recommendation generation, activity tracking, analytics, Redis caching, asynchronous background processing, and periodic recommendation refresh.

## Features

* User profile and music preference management
* Personalized song recommendations
* Spotify Web API integration
* Recommendation scoring based on:

  * Genre
  * Artist
  * Mood
  * Popularity
  * User activity
* Redis-based recommendation caching
* User activity tracking
* Analytics and trending data
* Celery asynchronous recommendation generation
* Celery Beat periodic recommendation refresh
* PostgreSQL persistence
* API rate limiting
* Dockerized development and production-style setup
* Nginx reverse proxy
* Gunicorn WSGI server
* Postman collection for API testing

## Architecture

```text
                         Client
                           |
                           v
                    +-------------+
                    |    Nginx    |
                    |    :8000    |
                    +------+------+
                           |
                           v
                    +-------------+
                    |  Gunicorn   |
                    |    Django   |
                    +------+------+
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
       PostgreSQL        Redis        Celery
                                         |
                                         v
                                   Spotify API

                    Celery Beat
                         |
                         v
                Periodic Recommendation
                     Refresh
```

## Tech Stack

| Technology            | Purpose                   |
| --------------------- | ------------------------- |
| Python 3.12           | Backend language          |
| Django                | Web framework             |
| Django REST Framework | REST APIs                 |
| PostgreSQL            | Persistent database       |
| Redis                 | Caching and Celery broker |
| Celery                | Background processing     |
| Celery Beat           | Periodic tasks            |
| Spotify Web API       | Music data                |
| Nginx                 | Reverse proxy             |
| Gunicorn              | WSGI application server   |
| Docker                | Containerization          |

## Project Structure

```text
Song_Recommendation_App/
│
├── activity/
├── analytics/
├── core/
├── recommendations/
├── users/
├── config/
│
├── nginx/
│   └── nginx.conf
│
├── postman/
│   └── Song-Recommendation-API.postman_collection.json
│
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── manage.py
├── pyproject.toml
├── requirements.txt
├── .env.example
└── README.md
```

## Prerequisites

Make sure the following are installed:

* Docker
* Docker Compose
* Git

For local development without Docker:

* Python 3.12+
* PostgreSQL
* Redis

## Environment Configuration

Create a `.env` file from `.env.example`.

Example:

```env
DEBUG=False

ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=Song_Discovery
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0

CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

SECURE_SSL_REDIRECT=False

SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

Do not commit `.env` or real API credentials to GitHub.

## Running with Docker

Build and start the complete application:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

Run migrations:

```bash
docker compose exec web python manage.py migrate
```

Configure the periodic recommendation refresh:

```bash
docker compose exec web python manage.py setup_periodic_tasks
```

View application logs:

```bash
docker compose logs -f web
```

View Celery logs:

```bash
docker compose logs -f celery
```

View Celery Beat logs:

```bash
docker compose logs -f celery-beat
```

The API is available at:

```text
http://localhost:8000
```

## API Endpoints

### Users

#### Create / Update User

```http
POST /api/v1/users/
```

Creates or updates a user profile and music preferences.

#### Get User

```http
GET /api/v1/users/{user_id}/
```

Returns user profile and preference information.

---

### Recommendations

#### Refresh Recommendations

```http
POST /api/v1/recommendations/{user_id}/refresh/
```

Queues an asynchronous recommendation refresh using Celery.

Response:

```json
{
    "message": "Recommendation refresh started.",
    "task_id": "celery-task-id",
    "user_id": "user-id"
}
```

#### Get Recommendations

```http
GET /api/v1/recommendations/{user_id}/
```

Returns the user's recommendations.

Recommendations are cached using Redis.

---

### Activity

#### Create Activity

```http
POST /api/v1/activity/activity-create/
```

Records user activity such as:

* PLAY
* LIKE
* SKIP
* COMPLETE

#### Get User Activity

```http
GET /api/v1/activity/?user={user_id}
```

Returns activity history for a user.

#### Activity Summary

```http
GET /api/v1/activity/summary/?user={user_id}
```

Returns activity statistics for a user.

---

### Analytics

#### Overall Analytics

```http
GET /api/v1/analytics/overall/
```

Returns application-wide activity statistics.

#### Trending Data

```http
GET /api/v1/analytics/trends/
```

Returns trending genres and artists.

Optional:

```text
/api/v1/analytics/trends/?limit=10
```

#### User Analytics

```http
GET /api/v1/analytics/user/{user_id}/
```

Returns analytics for an individual user.

## Recommendation System

Recommendations are generated using a scoring-based approach.

The scoring system considers:

```text
Genre match
Artist match
Mood match
Popularity
User activity
```

User activity such as likes, plays, and skips can influence recommendation scores.

The highest-scoring tracks are stored as recommendations for the user.

## Redis Caching

Redis is used for recommendation caching.

The recommendation flow is:

```text
GET Recommendations
        |
        v
   Redis Cache
      /    \
    HIT     MISS
     |        |
     v        v
 Response   PostgreSQL/
            Recommendation Service
                 |
                 v
            Store in Redis
                 |
                 v
              Response
```

Recommendation cache is invalidated when new recommendations are generated.

Redis databases are separated by purpose:

```text
Redis DB 0 -> Application cache
Redis DB 1 -> Celery broker
Redis DB 2 -> Celery result backend
```

## Celery Background Processing

Recommendation generation is performed asynchronously.

```text
API Request
    |
    v
Celery Task
    |
    v
Recommendation Service
    |
    v
Spotify / Recommendation Processing
    |
    v
PostgreSQL
    |
    v
Redis Cache Invalidation
```

This prevents long-running recommendation generation from blocking the API request.

## Celery Beat

Celery Beat periodically queues recommendation refresh tasks for active users.

The current periodic task runs every hour.

```text
Celery Beat
     |
     v
refresh_all_user_recommendations
     |
     +----> User 1 refresh task
     |
     +----> User 2 refresh task
     |
     +----> User 3 refresh task
```

## Analytics

The analytics module provides:

* Total activities
* Total users
* Total tracks
* Total plays
* Total likes
* Total skips
* Total completions
* Unique tracks played
* Most played tracks
* Trending genres
* Trending artists
* User-specific activity analytics

## Rate Limiting

The API uses Django REST Framework throttling.

Default limits:

```text
Authenticated users: 100 requests/hour
Anonymous users:      30 requests/hour

Recommendation refresh - authenticated: 10/hour
Recommendation refresh - anonymous:       5/hour
```

Recommendation refresh has a stricter rate limit because it triggers background processing.

## Postman Collection

A Postman collection is included in:

```text
postman/Song-Recommendation-API.postman_collection.json
```

Import the collection into Postman.

The collection uses:

```text
base_url = http://localhost:8000
```

All major API endpoints are included for testing.

## Makefile

Common commands:

```bash
make up
```

Start the application.

```bash
make build
```

Build images and start the application.

```bash
make down
```

Stop the application.

```bash
make migrate
```

Run Django migrations.

```bash
make makemigrations
```

Create migrations.

```bash
make logs
```

View all service logs.

```bash
make logs-web
```

View Django/Gunicorn logs.

```bash
make logs-celery
```

View Celery worker logs.

```bash
make logs-beat
```

View Celery Beat logs.

```bash
make shell
```

Open the Django shell.

```bash
make ps
```

View running containers.

## Docker Services

The Docker Compose configuration contains:

| Service     | Purpose                 |
| ----------- | ----------------------- |
| web         | Django + Gunicorn       |
| nginx       | Reverse proxy           |
| postgres    | PostgreSQL database     |
| redis       | Redis cache/broker      |
| celery      | Celery worker           |
| celery-beat | Periodic task scheduler |

## Production Considerations

The application uses a production-style architecture with:

* Gunicorn instead of Django development server
* Nginx reverse proxy
* Environment-based configuration
* PostgreSQL
* Redis
* Celery
* Docker containers
* API throttling

HTTPS should be configured at the deployment/load-balancer layer before enabling:

```text
SECURE_SSL_REDIRECT=True
```

Secrets such as Spotify credentials and database passwords should be supplied through environment variables.

## Future Improvements

Possible future improvements include:

* Automated test coverage
* CI/CD pipeline
* HTTPS configuration
* Health-check endpoints
* Improved recommendation algorithms
* Recommendation model personalization
* Spotify token refresh handling
* Monitoring and centralized logging
* API documentation with OpenAPI/Swagger
* Horizontal scaling of Celery workers

## Postman Testing

Recommended testing flow:

```text
1. Create User
       |
       v
2. Create Activity
       |
       v
3. Refresh Recommendations
       |
       v
4. Get Recommendations
       |
       v
5. Get Activity Summary
       |
       v
6. Get Analytics
       |
       v
7. Get Trends
```

## License

This project was developed as a backend engineering challenge and demonstration project.
