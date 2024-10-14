# API Sample Usage

## Introduction

The Campaign Analytics Platform provides four main API endpoints that allow users to interact with campaign data. The following documentation describes how to use each API endpoint, including the URL, input JSON request (if applicable), output JSON response for successful operations (HTTP 200), and error responses.

## 1. Get All Campaigns

**URL**: `http://127.0.0.1:8800/campaigns`

**Method**: `GET`

**Example**:

```bash
curl --location 'http://127.0.0.1:8800/campaigns'
```

**Output JSON Response (200)**:

```json
[
  {
    "campaign_name": "Campaign A",
    "number_of_ad_groups": 3,
    "ad_groups": [
      {
        "ad_group_name": "Ad Group 1",
        "average_cost": 100.50,
        "average_conversions": 5
      },
      {
        "ad_group_name": "Ad Group 2",
        "average_cost": 200.75,
        "average_conversions": 8
      }
    ],
    "average_monthly_cost": 150.63,
    "average_cost_per_conversion": 50.21
  }
]
```

**Error JSON Response**:

- If there is an internal server error:
  ```json
  {
    "detail": "Internal Server Error"
  }
  ```

## 2. Update Campaign Name

**URL**: `http://127.0.0.1:8800/campaigns/update-name/{campaign_id}`

**Method**: `PATCH`

**Example**:

```bash
curl --location --request PATCH 'http://127.0.0.1:8800/campaigns/update-name/20776040369' \
--header 'Content-Type: application/json' \
--data '{
  "name": "Footwear"
}'
```

**Input JSON Request**:

```json
{
  "name": "Footwear"
}
```

**Output JSON Response (200)**:

```json
{
  "message": "Campaign name updated successfully"
}
```

**Error JSON Response**:

- If the campaign ID is not found:
  ```json
  {
    "detail": "Campaign not found"
  }
  ```
- If there is an internal server error:
  ```json
  {
    "detail": "Internal Server Error"
  }
  ```

## 3. Get Performance Time Series Data

**URL**: `http://127.0.0.1:8800/performance-time-series?aggregate_by=month`

**Method**: `GET`

**Example**:

```bash
curl --location 'http://127.0.0.1:8800/performance-time-series?aggregate_by=month'
```

**Query Parameters**:

- `aggregate_by` (mandatory): Aggregate data by `day`, `week`, or `month`.

**Output JSON Response (200)**:

```json
{
  "data": [
    {
      "period": "2024-09-01T00:00:00+00:00",
      "total_cost": 4382.47,
      "total_clicks": 4397,
      "total_conversions": 364.24,
      "avg_cost_per_click": 1.0,
      "avg_cost_per_conversion": 12.03,
      "avg_click_through_rate": 0.01,
      "avg_conversion_rate": 0.08
    },
    {
      "period": "2024-08-01T00:00:00+00:00",
      "total_cost": 8212.51,
      "total_clicks": 4727,
      "total_conversions": 735.52,
      "avg_cost_per_click": 1.74,
      "avg_cost_per_conversion": 11.17,
      "avg_click_through_rate": 0.01,
      "avg_conversion_rate": 0.16
    }
  ]
}
```

**Error JSON Response**:

- If there is an internal server error:
  ```json
  {
    "detail": "Internal Server Error"
  }
  ```

## 4. Compare Campaign Performance

**URL**: `http://127.0.0.1:8800/compare-performance?start_date=2024-05-15&end_date=2024-05-21&compare_mode=preceding`

**Method**: `GET`

**Example**:

```bash
curl --location 'http://127.0.0.1:8800/compare-performance?start_date=2024-05-15&end_date=2024-05-21&compare_mode=preceding'
```

**Query Parameters**:

- `start_date` (required): Start date for the comparison period in `YYYY-MM-DD` format.
- `end_date` (required): End date for the comparison period in `YYYY-MM-DD` format.
- `compare_mode` (required): Comparison mode, either `preceding` or `previous_month`.

**Output JSON Response (200)**:

```json
{
  "current_period": {
    "start_date": "2024-05-15",
    "end_date": "2024-05-21",
    "cost_per_click": 2.93,
    "cost_per_conversion": 13.03,
    "cost_per_mille_impression": 210.55,
    "conversion_rate": 23.0,
    "click_through_rate": 7.17,
    "total_conversions": 108.36,
    "total_cost": 1411.56,
    "total_clicks": 481
  },
  "before_period": {
    "start_date": "2024-05-08",
    "end_date": "2024-05-14",
    "cost_per_click": 2.09,
    "cost_per_conversion": 16.64,
    "cost_per_mille_impression": 127.58,
    "conversion_rate": 13.0,
    "click_through_rate": 6.1,
    "total_conversions": 71.25,
    "total_cost": 1185.62,
    "total_clicks": 567
  },
  "comparison": {
    "cost_per_click": {
      "current": 2.93,
      "before": 2.09,
      "percent_change": 40.19
    },
    "cost_per_conversion": {
      "current": 13.03,
      "before": 16.64,
      "percent_change": -21.69
    },
    "cost_per_mille_impression": {
      "current": 210.55,
      "before": 127.58,
      "percent_change": 65.03
    },
    "conversion_rate": {
      "current": 23.0,
      "before": 13.0,
      "percent_change": 76.92
    },
    "click_through_rate": {
      "current": 7.17,
      "before": 6.1,
      "percent_change": 17.54
    },
    "total_conversions": {
      "current": 108.36,
      "before": 71.25,
      "percent_change": 52.08
    },
    "total_cost": {
      "current": 1411.56,
      "before": 1185.62,
      "percent_change": 19.06
    },
    "total_clicks": {
      "current": 481,
      "before": 567,
      "percent_change": -15.17
    }
  }
}
```

**Error JSON Response**:

- If there is an internal server error:
  ```json
  {
    "detail": "Internal Server Error"
  }
  ```

## Conclusion

This document provides a detailed overview of how to use each of the four main API endpoints, including the URL, request body (if applicable), and possible responses. The APIs are designed to provide an easy way to manage campaigns and view their performance metrics, making it convenient to interact with the Campaign Analytics Platform.