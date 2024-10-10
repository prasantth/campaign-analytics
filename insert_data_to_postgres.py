import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Load Excel data
file_path = 'Kaya_Hometask_Data_Nike.xlsx'
xls = pd.ExcelFile(file_path)

# Load the sheets into DataFrames
ad_group_df = pd.read_excel(xls, sheet_name='ad_group')
campaign_df = pd.read_excel(xls, sheet_name='campaign')
ad_group_stats_df = pd.read_excel(xls, sheet_name='ad_group_stats')

# Connect to PostgreSQL
# Get configs from .env file
connection = psycopg2.connect(
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
cursor = connection.cursor()

# Create campaign table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS campaign (
        campaign_id BIGINT PRIMARY KEY,
        campaign_name VARCHAR(255) NOT NULL,
        campaign_type VARCHAR(50) NOT NULL
    );
''')

# Create ad_group table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ad_group (
        ad_group_id BIGINT PRIMARY KEY,
        ad_group_name VARCHAR(255) NOT NULL,
        campaign_id BIGINT NOT NULL,
        FOREIGN KEY (campaign_id) REFERENCES campaign(campaign_id) ON DELETE CASCADE
    );
''')

# Create ad_group_stats table
cursor.execute('''
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
''')

# Insert data into campaign table
for _, row in campaign_df.iterrows():
    cursor.execute('''
        INSERT INTO campaign (campaign_id, campaign_name, campaign_type)
        VALUES (%s, %s, %s)
        ON CONFLICT (campaign_id) DO NOTHING;
    ''', (row['campaign_id'], row['campaign_name'], row['campaign_type']))

# Insert data into ad_group table
for _, row in ad_group_df.iterrows():
    cursor.execute('''
        INSERT INTO ad_group (ad_group_id, ad_group_name, campaign_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (ad_group_id) DO NOTHING;
    ''', (row['ad_group_id'], row['ad_group_name'], row['campaign_id']))

# Insert data into ad_group_stats table
for _, row in ad_group_stats_df.iterrows():
    cursor.execute('''
        INSERT INTO ad_group_stats (date, ad_group_id, device, impressions, clicks, conversions, cost)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    ''', (row['date'], row['ad_group_id'], row['device'], row['impressions'], row['clicks'], row['conversions'], row['cost']))

# Commit and close connection
connection.commit()
cursor.close()
connection.close()

print("Data inserted successfully!")
