# PostgreSQL Data Insertion Script

## Overview

This script, `insert_data_to_postgres.py`, automates the process of creating tables in a PostgreSQL database and populating them with data from an Excel spreadsheet. The script includes:

- Connecting to a PostgreSQL database using credentials from a `.env` file.
- Creating three tables (`campaign`, `ad_group`, and `ad_group_stats`) if they do not exist.
- Inserting data into these tables from respective sheets in the Excel file.
- Handling potential conflicts during data insertion.

## Prerequisites

Before running this script, ensure you have the following installed:

- Python 3.10 or higher
- PostgreSQL server
- Python libraries:
  
  ```bash
  pip install psycopg2-binary pandas python-dotenv
  ```

- A `.env` file with the following content:

  ```bash
  DB_NAME=nike_campaign_data
  DB_USER=postgres
  DB_PASSWORD=postgres
  DB_HOST=localhost
  DB_PORT=5432
  ```

## Excel Data

Ensure that the Excel file `Kaya_Hometask_Data_Nike.xlsx` is present in the same directory as the script. The Excel file should contain three sheets:

- `ad_group`
- `campaign`
- `ad_group_stats`

## Script Explanation

### 1. Load Environment Variables

The script uses `python-dotenv` to load database configuration from the `.env` file:

```python
from dotenv import load_dotenv
load_dotenv()
```

### 2. Load Data from Excel

Reads data from the Excel file using `pandas`:

```python
file_path = 'Kaya_Hometask_Data_Nike.xlsx'
xls = pd.ExcelFile(file_path)

ad_group_df = pd.read_excel(xls, sheet_name='ad_group')
campaign_df = pd.read_excel(xls, sheet_name='campaign')
ad_group_stats_df = pd.read_excel(xls, sheet_name='ad_group_stats')
```

### 3. Connect to PostgreSQL

Connects to the PostgreSQL database using `psycopg2` with credentials from the `.env` file:

```python
connection = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cursor = connection.cursor()
```

### 4. Create Tables

The script creates three tables if they do not exist:

- **`campaign` Table**: Stores campaign information.
- **`ad_group` Table**: Stores ad groups, with a foreign key reference to `campaign`.
- **`ad_group_stats` Table**: Stores performance statistics for each ad group.

```sql
CREATE TABLE IF NOT EXISTS campaign (
    campaign_id BIGINT PRIMARY KEY,
    campaign_name VARCHAR(255) NOT NULL,
    campaign_type VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS ad_group (
    ad_group_id BIGINT PRIMARY KEY,
    ad_group_name VARCHAR(255) NOT NULL,
    campaign_id BIGINT NOT NULL,
    FOREIGN KEY (campaign_id) REFERENCES campaign(campaign_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ad_group_stats (
    stats_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    ad_group_id BIGINT NOT NULL,
    device VARCHAR(50) NOT NULL,
    impressions DECIMAL(10, 2) NOT NULL,
    clicks INT NOT NULL,
    conversions DECIMAL(10, 2) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (ad_group_id) REFERENCES ad_group(ad_group_id) ON DELETE CASCADE
);
```

### 5. Insert Data into Tables

Inserts data from the Excel DataFrames into the PostgreSQL tables:

- **Insert into `campaign`**:

  ```python
  for _, row in campaign_df.iterrows():
      cursor.execute('''
          INSERT INTO campaign (campaign_id, campaign_name, campaign_type)
          VALUES (%s, %s, %s)
          ON CONFLICT (campaign_id) DO NOTHING;
      ''', (row['campaign_id'], row['campaign_name'], row['campaign_type']))
  ```

- **Insert into `ad_group`**:

  ```python
  for _, row in ad_group_df.iterrows():
      cursor.execute('''
          INSERT INTO ad_group (ad_group_id, ad_group_name, campaign_id)
          VALUES (%s, %s, %s)
          ON CONFLICT (ad_group_id) DO NOTHING;
      ''', (row['ad_group_id'], row['ad_group_name'], row['campaign_id']))
  ```

- **Insert into `ad_group_stats`**:

  ```python
  for _, row in ad_group_stats_df.iterrows():
      cursor.execute('''
          INSERT INTO ad_group_stats (date, ad_group_id, device, impressions, clicks, conversions, cost)
          VALUES (%s, %s, %s, %s, %s, %s, %s);
      ''', (row['date'], row['ad_group_id'], row['device'], row['impressions'], row['clicks'], row['conversions'], row['cost']))
  ```

### 6. Commit and Close the Connection

After inserting the data, the script commits the transactions and closes the connection:

```python
connection.commit()
cursor.close()
connection.close()
print("Data inserted successfully!")
```

## Running the Script

1. Ensure PostgreSQL is running and the `.env` file is properly configured.
2. Run the script with:

   ```bash
   python insert_data_to_postgres.py
   ```

3. Verify the inserted data by running the following queries in PostgreSQL:

   ```sql
   SELECT * FROM campaign;
   SELECT * FROM ad_group;
   SELECT * FROM ad_group_stats;
   ```

## Troubleshooting

- Ensure the PostgreSQL server is running.
- Verify that the `.env` file contains the correct credentials.
- Check the path to the Excel file and ensure it matches `file_path` in the script.
