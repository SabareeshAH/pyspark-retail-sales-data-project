"""
File Name: bronze_layer_data_processing.py

Description:
    This PySpark file is used for Bronze layer data processing.
    The file defines the source data schema and data types for
    ingesting raw data into the Bronze layer.

Processing:
    -> Defines explicit schema with required data types.
    -> Loads raw source data into the Bronze layer.
    -> Performs only schema enforcement and basic ingestion.
    -> No data cleansing or business transformations are applied.

Layer:
    Bronze Layer (Raw Data Layer)

Schema:
    -> Explicit data types are defined to ensure data consistency during ingestion.
    -> No data cleansing or business rules are applied at this stage.
"""

#/***************************************************************************\
# Required Headers
#\***************************************************************************/
from pyspark.sql.types import(StructType, StructField, IntegerType, DoubleType, StringType, DateType)

#/***************************************************************************\
# Schema Definition
#\***************************************************************************/
bronze_schema = ( StructType([
StructField("transaction_id", IntegerType(), True),
StructField("order_date", DateType(), True),
StructField("ship_date", DateType(), True),
StructField("customer_id", StringType(), True),
StructField("customer_age", IntegerType(), True),
StructField("gender", StringType(), True),
StructField("product_id", StringType(), True),
StructField("product_category", StringType(), True),
StructField("quantity", IntegerType(), True),
StructField("unit_price", DoubleType(), True),
StructField("discount_percentage", DoubleType(), True),
StructField("city", StringType(), True),
StructField("state", StringType(), True),
StructField("payment_type", StringType(), True),
StructField("order_status", StringType(), True),
StructField("ingestion_date", DateType(), True)]))

#/***************************************************************************\
# Data Reading from CSV
#\***************************************************************************/
bronze_df = spark.read.option("header","true").schema(bronze_schema).csv("/opt/spark-data/raw/retail_sales_raw.csv")

bronze_df.count()

#/***************************************************************************\
# Schema Check
#\***************************************************************************/
bronze_df.printSchema()

#/***************************************************************************\
# Bronze Data (with Schema) Written as Parquet 
#\***************************************************************************/
bronze_df.write.mode("overwrite").parquet("/opt/spark-data/transformed_data/bronze/retail_sales_bronze.parquet")