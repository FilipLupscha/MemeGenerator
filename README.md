## Running the Project with Docker

This project is containerized using Docker and can be run easily with Docker Compose. Below are the specific instructions and details for this setup:

### Project-Specific Docker Details
- **Base Image:** Uses `python:3.13-slim` for both build and runtime stages.
- **Virtual Environment:** Dependencies are installed in a Python virtual environment (`.venv`) inside the container.
- **Entrypoint:** The application starts with `python app.py`.

### Environment Variables
- No required environment variables are specified in the Dockerfile or Compose file. If you need to add any, uncomment the `env_file` line in `docker-compose.yml` and provide a `.env` file.

### Build and Run Instructions
1. **Build and start the service:**
   ```sh
   docker compose up --build
   ```
   This will build the image and start the `python-app` service.

2. **Access the application:**
   - The app will be available on [http://localhost:5000](http://localhost:5000)

### Ports
- **Exposed Port:** `5000` (mapped from container to host)

### Special Configuration
- No external services (databases, caches) or persistent volumes are required for this project.
- The container runs as a non-root user (`appuser`) for improved security.

---
*For any additional configuration, such as environment variables, update the `docker-compose.yml` and provide a `.env` file as needed.*