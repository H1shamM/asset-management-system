# Asset Management & Security Checks Microservice

This project provides a set of APIs for managing assets and performing security scans on them. The microservices are built using **Spring Boot** (Java) for the backend (security-service) and **Flask** (Python) for asset-service. The system provides endpoints for checking asset details and security scan results. **MongoDB** is used to store asset data, and **Redis** is used for caching.

## Features

### Security Endpoints

- `GET /security/scan/{assetId}`: Checks vulnerabilities for a specific asset.
- `GET /security/policy/{assetId}`: Checks if an asset complies with encryption policies.
- `POST /security/test`: Adds a test security scan result.

### Asset Management Endpoints

- `GET /assets`: Returns a list of all assets, including their security scan results.
- `POST /assets`: Adds a new asset with associated security scan results.

## Technologies

- **Spring Boot**: Java framework for building microservices.
- **MongoDB**: NoSQL database for storing asset and scan data.
- **Redis**: In-memory data store for caching.
- **Docker Compose**: For easy orchestration of services.
- **Flask**: Python framework for managing assets.

## Installation

### Prerequisites

Make sure you have the following installed:

- **Docker** and **Docker Compose** (for containerizing and orchestrating the application).

### Steps to Run Locally with Docker Compose

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/asset-management-system.git
    cd asset-management-system
    ```

2. **Run Docker Compose**:
    This will set up the environment and start all services (MongoDB, Redis, security-service, and asset-service).

    ```bash
    docker-compose up --build
    ```

3. **The services will be available at**:
    - Asset Service (Flask): `http://localhost:5000`
    - Security Service (Spring Boot): `http://localhost:8080`
    - MongoDB: `localhost:27017`
    - Redis: `localhost:6379`

4. **Access the services**:
    Once everything is running, you can interact with the services using `curl` or Postman.

## Usage

### 1. **POST an asset**

```bash
    curl -X POST http://localhost:5000/assets -H "Content-Type: application/json" -d '{
        "id": "server_001",
        "type": "VM",
        "owner": "IT",
        "status": "active",
        "tags": ["encrypted"],
        "security_scan": {"compliant": true, "findings": []}
    }'
    ```

### 2. **GET all assets**

    ```bash
    curl http://localhost:5000/assets
    ```

### 3. **POST a test security scan**

    ```bash
    curl -X POST http://localhost:8080/security/test -H "Content-Type: application/json" -d '{
        "assetId": "VM-123",
        "findings":[
            {"cveId":"VULN-1", "description":"First dummy vulnerability.","severity":"HIGH"},
            {"cveId":"VULN-2", "description":"Second dummy vulnerability.","severity":"MEDIUM"}
        ],
        "scannedAt":"2025-05-05T12:35:07.719258178Z",
        "compliant":true
    }'
    ```

### 4. **GET security scan result for an asset**

    ```bash
    curl http://localhost:8080/security/scan/server_001
    ```

## Running without Docker Compose

1. **Run MongoDB**:

    ```bash
    docker run -d -p 27017:27017 --name mongodb -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=example mongo:6.0
    ```

2. **Run Redis**:

    ```bash
    docker run -d -p 6379:6379 --name redis redis:alpine
    ```

3. **Run Flask (Asset Service)**:

    ```bash
    cd asset-service
    pip install -r requirements.txt
    flask run
    ```

4. **Run Spring Boot (Security Service)**:

    ```bash
    cd security-service
    mvn spring-boot:run
    ```

## Contributing

Feel free to fork and create pull requests! For any major changes, please open an issue first to discuss.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
