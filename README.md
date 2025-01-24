# Project README

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed on your system.
- Python 3.12 or later if running outside Docker.

### Steps to Set Up

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Start the services using Docker Compose:

   ```bash
   docker-compose up --build
   ```

3. Verify that the following services are running:

   - PostgreSQL (accessible at port 5432)
   - RabbitMQ (management UI at [http://localhost:15672](http://localhost:15672))
   - Redis (accessible at port 6379)
   - Ingestion Service (accessible at [http://localhost:8001](http://localhost:8001))
   - Alerting Service (accessible at [http://localhost:8002](http://localhost:8002))

4. Check the database setup:

   - Connect to PostgreSQL using a database client or CLI.
   - Ensure the tables (`users_authorization`, `alerts`, `events`) are created.

5. Test RabbitMQ initialization:

   - Visit the RabbitMQ management UI.
   - Verify the `events` queue is listed in the "Queues" tab.

### Environment Variables

The following environment variables are configured in the `docker-compose.yml` file:

| Variable       | Description                  | Example                             |
| -------------- | ---------------------------- | ----------------------------------- |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db`    |
| `RABBITMQ_URL` | RabbitMQ connection URL      | `amqp://guest:guest@rabbitmq:5672/` |
| `REDIS_HOST`   | Redis hostname               | `redis`                             |
| `REDIS_PORT`   | Redis port                   | `6379`                              |
| `DB_NAME`      | PostgreSQL database name     | `ametos`                            |
| `DB_USER`      | PostgreSQL username          | `postgres`                          |
| `DB_PASSWORD`  | PostgreSQL password          | `postgres`                          |
| `DB_HOST`      | PostgreSQL hostname          | `postgres`                          |
| `DB_PORT`      | PostgreSQL port              | `5432`                              |
| `RABIT_QUEUE`  | RabbitMQ queue name          | `events`                            |
| `RABIT_HOST`   | RabbitMQ hostname            | `rabbitmq`                          |

---

## API Endpoint Documentation

### Ingestion Service (Port 8001)

#### 1. **POST /event**

- **Description**: Ingests an event from a device.
- **Request Body (JSON)**:
  ```json
  {
    "device_id": "string",
    "device_type": "string",
    "timestamp": "ISO 8601 datetime",
    "event_type": "string",
    "speed_kmh": "integer",
    "location": "string",
    "zone": "string",
    "confidence": "float",
    "photo_base64": "base64 string",
    "user_id": "string"
  }
  ```
- **Response**:
  - `200 OK` on success.
  - `400 Bad Request` if the input is invalid.

#### 2. **GET /events**

- **Description**: Retrieves all events.
- **Response**:
  ```json
  [
    {
      "id": "integer",
      "device_id": "string",
      "device_type": "string",
      "timestamp": "ISO 8601 datetime",
      "event_type": "string",
      "speed_kmh": "integer",
      "location": "string",
      "zone": "string",
      "confidence": "float",
      "photo_base64": "base64 string",
      "user_id": "string"
    }
  ]
  ```

### Alerting Service (Port 8002)

#### 1. **GET /alerts**

- **Description**: Retrieves all active alerts.
- **Response**:
  ```json
  [
    {
      "id": "integer",
      "device_id": "string",
      "device_type": "string",
      "timestamp": "ISO 8601 datetime",
      "event_type": "string",
      "speed_kmh": "integer",
      "location": "string",
      "zone": "string",
      "confidence": "float",
      "photo_base64": "base64 string",
      "user_id": "string"
    }
  ]
  ```

---

## Explanation of Alert Criteria

The system generates alerts based on the following criteria:

1. **Speed Violation**:

   - An alert is triggered if the `speed_kmh` exceeds a predefined threshold for the specified `zone`.

2. **Confidence Threshold**:

   - An alert is generated if the `confidence` level of an event drops below a certain percentage (e.g., 50%).

3. **Unauthorized User**:

   - If an event is associated with a `user_id` that is not marked as `is_authorized` in the `users_authorization` table, an alert is triggered.

4. **Specific Event Types**:

   - Alerts are generated for certain `event_type` values (e.g., "accident", "intrusion") regardless of other parameters.

5. **Geofencing**:

   - If the `location` of an event falls outside an allowed `zone`, an alert is triggered.

---

