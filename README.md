# Test Task: Weather Query Web Application

## Author
Roman Kuzmich

## Objective
A simple web application that allows users to enter a city name, fetch current weather data from a public API, 
and store/display the query history. The application uses PostgreSQL to store user queries and the associated weather information.

## Stack
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Alembic**
- **Docker Compose**
- **Requests (external API calls)**
- **Redis (rate limiting and caching)**

## Quickstart with Docker Compose
1. Clone the repository
2. Copy environment variables from the sample, fill your OW_API_KEY in **.env** and **.env.docker**
3. Build and start all services (app, db, test_db, Redis):
```bash
docker compose build
docker compose up -d
```
4. Access the application:
- Swagger ui: http://localhost:8000/docs
5. Testing:
```bash
docker compose exec app pytest
```
6. Stop the services when done:
```bash
docker compose down
```