# Project Overview: Campaign Analytics Platform

## Introduction
This is an analytics platform designed to provide marketing performance insights using data from campaigns, ad groups, and associated metrics like clicks, impressions, conversions, and cost. The project leverages Python, FastAPI, and PostgreSQL to create an effective and scalable solution for analyzing campaign performance.

## Features
- **Campaign Performance Monitoring**: View and track details of different marketing campaigns and their ad groups, including cost and conversion metrics.
- **Time-Series Analytics**: Generate time-series performance data aggregated by day, week, or month for an in-depth understanding of campaign performance over time.
- **Comparative Analytics**: Compare current performance with preceding periods or previous months to understand trends and make informed decisions.
- **RESTful API**: The platform exposes RESTful APIs built using FastAPI for easy integration with other systems and automation tools.

## Project Structure
The project is organized to facilitate scalability, readability, and ease of maintenance:

- **src/**: Core application directory.
  - **models/**: SQLAlchemy models for representing database tables.
  - **database/**: Database connection and session handling logic.
  - **routers/**: API endpoints for various features such as campaign management and performance analytics.
  - **schemas/**: Pydantic models for request validation and serialization.
  - **analytics/**: Business logic and calculations for analytics features.
  - **utils/**: Utility functions like logging.

- **my-docs/**: Contains MkDocs documentation for understanding the project structure, setup, and usage.
- **test/**: Unit test to ensure the reliability of the application.
- **logs/**: Stores log files generated during the application's execution for monitoring and debugging.

## Installation
To set up the Campaign Analytics Platform on your local machine:

1. **Clone the repository**:

    ```bash
    git clone <repository-url>
    ```

2. **Navigate to the project directory**:
   ```bash
   cd kaya
   ```

3. **Install Docker**:
   Follow the instructions to install Docker on your machine from [Docker's official website](https://docs.docker.com/get-docker/).

4. **Build the Docker image**:
   ```bash
   docker build -t campaign-analytics .
   ```

5. **Run the Docker container**:
   ```bash
   docker run -d -p 8800:8800 -p 5500:5500 --name campaign-analytics campaign-analytics
   ```

6. **Access the API documentation**:
   Once the container is running, API documentation will be available at `http://localhost:8800/docs`.

7. **Access the Project documentation**:
   The project documentation will be available at `http://localhost:5500`.