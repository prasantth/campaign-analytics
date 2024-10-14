# Testing

## Introduction
Testing is an essential part of the development process to ensure the reliability and correctness of the Campaign Analytics Platform. For this project, `pytest` was used as the primary testing framework. `pytest` provides an easy-to-use syntax for writing both unit and integration tests, allowing the development team to thoroughly verify different parts of the application.

## Types of Tests Implemented

### 1. Unit Tests
Unit tests were created to validate the individual components of the application, such as:
- **Database Models**: Testing the SQLAlchemy models to ensure that database tables and relationships are defined correctly.
- **Utility Functions**: Testing utility functions, such as logging, to confirm they perform as expected in different scenarios.

These tests ensure that each function behaves correctly in isolation, reducing the likelihood of defects at the component level.

### 2. Integration Tests
Integration tests were done manually to verify the interactions between different components of the application, such as:
- **API Endpoints**: Testing the endpoints provided by the `campaigns` and `performance` routers to ensure that they return the correct responses, given valid and invalid inputs.
- **Database Interaction**: Testing the integration between the FastAPI application and the PostgreSQL database to verify that data is stored, retrieved, and modified correctly.

Integration tests help in verifying that different modules work well together and that the overall workflow is functioning correctly.

## Test Structure
The tests are organized into separate files to maintain clarity and modularity:

- **`test_campaigns.py`**: Contains unit and integration tests for the `campaigns` endpoints, such as creating, updating, and deleting campaigns.
- **`test_performance.py`**: Tests the performance-related endpoints, including retrieving time-series data and comparing metrics.
- **`test_database.py`**: Focuses on the correctness of database connections and model definitions, ensuring that tables are created and managed properly.
- **`conftest.py`**: Contains shared fixtures, such as setting up a test database, creating a FastAPI test client, and other reusable components.

These files are located in the `test/unit` directory, and shared configurations are maintained to facilitate easy test management.

## Running the Tests
To execute the tests, `pytest` is used, which automatically discovers all the test files and functions. The following command runs all the tests in the project:

```bash
pytest
```

The test results provide information about passing and failing tests, along with detailed error messages, making it easy to identify issues in the code.

For more detailed output, the following command can be used:

```bash
pytest -v
```

This command provides verbose output, which includes details about each test case and helps in troubleshooting any failures.

## Key Points
- **Fixtures**: `pytest` fixtures are used to set up and tear down resources needed for tests, such as database connections and test clients. This helps in maintaining clean and isolated test environments.
- **Coverage**: To ensure that all parts of the application are tested, code coverage tools can be used along with `pytest`. This helps in identifying any parts of the code that may not have sufficient test coverage.
- **Automation**: The tests are designed to be run automatically as part of the CI/CD pipeline, ensuring that changes made to the codebase do not introduce regressions.

## Conclusion
The use of `pytest` for testing the Campaign Analytics Platform ensures that the application is reliable and that any defects are caught early in the development process. By writing both unit and integration tests, the project maintains a high level of quality, ensuring that all functionalities perform as expected.

