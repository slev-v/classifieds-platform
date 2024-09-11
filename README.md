# FastAPI User Management Project

## Overview

This is a FastAPI project designed for user management with basic authentication functionalities. It includes features such as user creation and deletion. The project is containerized using Docker and Docker Compose for streamlined setup and deployment. The `classifieds` feature is still under development.

## Features

This project uses a microservices architecture with separate services for user management and classifieds. Each service operates independently, ensuring modularity and scalability.

- **User Service**: Manages user authentication and related operations.
- **Classified Service**: Handles classified ads and their related functionalities.

Both services follow **Domain-Driven Design (DDD)** principles to organize code around domain models and business logic.

**Event-Driven Architecture**: Kafka is used for asynchronous communication between services, facilitating real-time data processing and integration.

## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

## How to Use

1. **Clone the repository:**

   ```bash
   git clone <https://github.com/your_username/your_repository.git>
   cd your_repository
   ```

2. **Set up the environment and start the services:**

- Firstly, start kafka with:

    ```bash
    make kafka
    ```

- Then you can start storages with:

    ```bash
    make user-storages
    make classified-storages
    ```

- Make migrations with:

    ```bash
    make user-migrate
    make classified-migrate
    ```

- Finally, start the applications with:

    ```bash
    make user-dev
    make classified-dev
    ```

## Notes

- Ensure your `.env` file is configured correctly for Docker Compose.
- The `classifieds` feature is still under development and not yet available.
