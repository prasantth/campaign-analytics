# API Development

## Introduction
The API for the Campaign Analytics Platform has been developed using FastAPI, a modern web framework for Python that enables rapid development of RESTful APIs. The main objectives of the API are to provide easy access to campaign performance data, support different analytics features, and expose endpoints for integration with other systems.

## Application Structure
The FastAPI app has been structured into different modules to maintain scalability and readability. The primary modules used in the app include:

- **Database Module**: The database connection and table creation are handled by SQLAlchemy, using the `Base` and `engine` objects imported from `src.database.database`.
- **Routers**: The APIs are grouped by functionalities, such as campaigns and performance, and are placed in dedicated routers. These routers are included in the main FastAPI app, allowing a modular approach to adding new features.
- **Logging**: A logging utility (`Log`) is used to record key events such as application startup and API requests.

## API Details
1. **Campaign Management**: The `campaigns` router provides endpoints to manage marketing campaigns. These endpoints allow users to:
      - Update campaign name.

2. **Performance Analytics**: The `performance` router exposes endpoints for retrieving performance metrics of campaigns, including:
   - Getting time-series data (e.g., impressions, clicks, conversions) for specified date ranges.
   - Comparing current performance against historical data to generate insights for decision-making.

The `main.py` file includes both routers, allowing users to interact with different sections of the campaign data seamlessly.

## FastAPI Main Application
The entry point of the API is the `main.py` file, which performs the following functions:

- Initializes the FastAPI application.
- Includes the routers for campaigns and performance.
- Uses `Uvicorn` to run the FastAPI app.

The application starts by creating necessary tables using SQLAlchemy's `Base.metadata.create_all()` function, ensuring that the database schema is up-to-date. Next, the app includes routers from the campaigns and performance modules, which makes the corresponding endpoints accessible to users.

## Running the API
The API can be started using `Uvicorn`, which is configured to run on host `0.0.0.0` and port `8800`.

To run the FastAPI app, use the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8800
```

The logging module is used to log the application start and any interactions, which helps in monitoring the system and troubleshooting issues.

## Key Points
- The API is modular, consisting of dedicated routers for managing campaigns and analyzing performance.
- SQLAlchemy is used to manage the database, and tables are created automatically at the application startup.
- The application uses logging to keep track of key events, improving the maintainability of the system.

## Conclusion
This API provides a comprehensive way to interact with campaign data, enabling seamless management and analytics. By leveraging FastAPI, it provides a performant and easy-to-use interface for external integration and automation.

