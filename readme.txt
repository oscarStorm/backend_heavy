Backend-Heavy Booking System
A small backend architecture experiment that explores what happens when business rules are handled primarily in Python rather than in the database.

This project is one half of a comparison with database_heavy. Both implementations model the same booking system, but place responsibility for validation and business logic in different layers.
Features
- Create and list customers
- Create and list bookable resources (such as tables)
- Create and list bookings
- Check which resources are available for a requested time period
- Cancel bookings
Tech Stack
- Python and FastAPI — HTTP API
- Pydantic — request validation
- MySQL 8.4 — relational data storage
- PyMySQL — direct SQL access from Python
- Textual — terminal-based user interface
- HTTPX — HTTP requests from the terminal client to the API
- Docker Compose — local MySQL instance
The project deliberately avoids an ORM. Using direct SQL makes it easier to compare the two implementations without introducing differences caused by an ORM.
Architecture
Textual terminal UI
        |
       HTTPX
        |
     FastAPI
        |
Pydantic validation
        |
Python business logic
        |
  PyMySQL / SQL
        |
      MySQL
In this version, the Python backend is intended to make business decisions before writing data to MySQL. The database is primarily responsible for persistence and relational integrity.

The database-heavy version takes a different approach: stored procedures, triggers and database constraints enforce most of the domain rules.
Project Structure
app/                 Application code and terminal client
scripts/             Project scripts
sql/                 SQL definitions and setup files
tests/               Test code
docker-compose.yml   MySQL development container
requirements.txt     Python dependencies
Getting Started
Requirements: Python, Docker and Docker Compose.
1. Clone the repository and install the Python dependencies:
   git clone https://github.com/oscarStorm/backend_heavy.git
   cd backend_heavy
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
2. Create a .env file at the repository root with the variables required by docker-compose.yml:
   MYSQL_ROOT_PASSWORD=change-me-root
   MYSQL_DATABASE=booking_db
   MYSQL_USER=booking_user
   MYSQL_PASSWORD=change-me
   These are example local-development credentials. Use the database connection settings expected by the application code as well.
3. Start MySQL:
   docker compose up -d
   The container exposes MySQL on localhost:3306. The Compose file starts the database only; it does not start the API or terminal UI.
4. Initialize the database using the SQL/setup files in sql/ and scripts/, then start the FastAPI application and terminal client from app/.
   Note: The precise API, terminal-client and database-initialization commands have not been verified here; check the corresponding entry points before running them.
What This Experiment Explores
Keeping domain rules in Python makes them straightforward to read, test and evolve alongside the API. It also raises questions about consistency if another service writes directly to the same database, and about handling concurrent booking requests safely.

The goal is to compare these trade-offs with a version that puts more responsibility in MySQL, not to declare one approach universally better.
Related Project
database_heavy — the same booking use cases, implemented with MySQL stored procedures, triggers and constraints handling most business rules.
