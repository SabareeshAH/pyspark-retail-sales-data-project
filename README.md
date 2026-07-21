# Retail Sales Analysis Data Project using Apache Spark

## Overview

This project demonstrates a modern **Data Engineering ETL pipeline** built using **Apache Spark (PySpark)** to process retail sales data through a **Medallion Architecture (Bronze → Silver → Gold)**. The pipeline ingests raw CSV data, performs data cleaning and transformations, generates business-ready analytical datasets, and presents key sales metrics through a lightweight dashboard.

The primary objective of this project is to showcase scalable data processing practices, layered data architecture, and business-oriented data modeling using Apache Spark.

---

## Project Architecture

```
Random Data Generator
        │
        ▼
   Raw CSV Files
        │
        ▼
┌───────────────────┐
│ Bronze Layer      │
│ Schema Definition │
└───────────────────┘
        │
        ▼
┌────────────────────────────┐
│ Silver Layer               │
│ Data Cleaning              │
│ Data Transformation        │
│ Data Standardization       │
└────────────────────────────┘
        │
        ▼
┌────────────────────────────┐
│ Gold Layer                 │
│ Business Ready Data        │
│ • Overall Sales            │
│ • Product Sales            │
│ • City-wise Sales          │
└────────────────────────────┘
        │
        ▼
 Basic Sales Dashboard
```

---

## Tech Stack

| Technology                 | Purpose                                     |
| -------------------------- | ------------------------------------------- |
| **Apache Spark (PySpark)** | Distributed data processing                 |
| **Docker Desktop**         | Running Spark environment                   |
| **Python**                 | Data generation                             |
| **Visual Studio Code**     | Development and code editing                |
| **Terminal**               | Executing PySpark applications              |
| **Parquet**                | Optimized storage format for processed data |

---
## Project Architecture

<img width="1352" height="275" alt="image" src="https://github.com/user-attachments/assets/5a194388-6e22-45e5-ab61-a4f99a65b02b" />

## Project Workflow

### Step 1 – Data Generation

Retail sales data is generated using a custom Python script:

```
random_data_generator.py
```

The generated dataset is stored in **CSV format**, simulating raw transactional sales data.

---

### Step 2 – Bronze Layer

The Bronze layer represents the raw ingestion stage.

#### Activities

* Read raw CSV files
* Define explicit Spark schema
* Validate input structure
* Store processed output in Parquet format

**Output Format**

```
Parquet
```

---

### Step 3 – Silver Layer

The Silver layer focuses on improving data quality.

#### Activities

* Handle missing values
* Clean invalid records
* Apply business transformations
* Standardize data types
* Prepare analytics-ready dataset

**Output Format**

```
Parquet
```

---

### Step 4 – Gold Layer

The Gold layer contains business-ready aggregated datasets optimized for reporting and analytics.

The following datasets are created:

### Overall Sales

Provides organization-wide sales metrics.

### Product Sales

Summarizes sales performance by product.

### City-wise Sales

Aggregates sales across different cities.

Each Gold dataset is stored in **Parquet** format for efficient querying and downstream analytics.

---

## Data Storage Strategy

The project follows a layered storage approach.

| Layer  | Input          | Output  |
| ------ | -------------- | ------- |
| Bronze | CSV            | Parquet |
| Silver | Bronze Parquet | Parquet |
| Gold   | Silver Parquet | Parquet |

Each processing layer reads the Parquet output from the previous layer, enabling a modular, scalable, and maintainable ETL pipeline.

---

## Dashboard

A lightweight dashboard is built using the Gold layer datasets to demonstrate the processed business metrics.

The dashboard includes basic sales summaries such as:

* Overall Sales
* Product-wise Sales
* City-wise Sales

The objective is to validate the Gold layer outputs rather than provide advanced business intelligence visualizations.

### Dashboard Image

<img width="921" height="516" alt="image" src="https://github.com/user-attachments/assets/7ba8047b-c316-4b13-910e-f91b9e0aefdd" />

---

## Project Structure

```
Retail-Sales-Analysis/
│
├── dashboard/
│
├── data_source/
│   ├── random_data_generator.py
│
├── generated_data/raw
│   ├──retail_sales_raw.csv
│
├── pyspark_codes/
│   ├──bronze_layer_data_processing.py
│   ├──silver_layer_data_processing.py
│   ├──gold_layer_data_processing.py
│
├── README.md
```

---

## Key Features

* Medallion Architecture (Bronze, Silver, Gold)
* Apache Spark data processing
* Schema enforcement
* Data cleaning and transformation
* Layered ETL pipeline
* Parquet-based storage
* Business-level aggregated datasets
* Docker-based Spark environment
* Simple analytical dashboard
* Modular and maintainable project structure

---

## How to Run

### 1. Start Docker Desktop

Ensure Docker Desktop is running with the Apache Spark environment.

### 2. Generate Sample Data

```bash
python random_data_generator.py
```

### 3. Execute Bronze Layer

```bash
spark-submit bronze_layer.py
```

### 4. Execute Silver Layer

```bash
spark-submit silver_layer.py
```

### 5. Execute Gold Layer

```bash
spark-submit gold_layer.py
```

### 6. Launch the Dashboard

Run the dashboard application to visualize the Gold layer datasets.

---

## Future Enhancements

* Integration with cloud object storage (AWS S3, Azure Data Lake, or Google Cloud Storage)
* Workflow orchestration using Apache Airflow
* Delta Lake implementation
* Data quality validation using Great Expectations
* Incremental data processing
* Spark Structured Streaming
* Interactive dashboards using Power BI or Tableau
* CI/CD pipeline using GitHub Actions

---

## Learning Outcomes

This project demonstrates practical implementation of:

* Apache Spark (PySpark)
* Data Engineering ETL pipelines
* Medallion Architecture
* Data transformation techniques
* Parquet storage optimization
* Business data modeling
* Docker-based development environment
* Layered data processing architecture

---

## License

This project is intended for educational and portfolio purposes.
