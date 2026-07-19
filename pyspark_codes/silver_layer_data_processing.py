"""
File Name: silver_layer_data_processing.py

Description:
    This PySpark file is used for Silver layer data processing.
    It performs data cleaning, validation, and transformation on
    Bronze layer data to create refined and reliable datasets.

Processing:
    -> Reads raw data from the Bronze layer.
    -> Applies data cleansing rules and data quality checks.
    -> Handles null values, duplicates, and incorrect data formats.
    -> Applies required data transformations and standardization.
    -> Creates cleaned and structured data for downstream consumption.

Layer:
    Silver Layer (Cleansed/Refined Data)
"""

#/***************************************************************************\
# Required Headers
#\***************************************************************************/
from pyspark.sql.functions import col, when, trim

#/***************************************************************************\
# Data Reading from bronze layer parquet file
#\***************************************************************************/
broze_df = spark.read.parquet("/opt/spark-data/transformed_data/bronze/retail_sales_bronze.parquet")

# -----------------------------------------------------------------------------
# DATA CLEANING AND TRANSFORMATION
# -----------------------------------------------------------------------------

#/***************************************************************************\
# Seeing the duplicate transactions ids (explicitly seeing 1st 10)
#\***************************************************************************/
bronze_df.groupBy("transaction_id").count().filter(col("count") > 1).show(10, truncate=False)

#/***************************************************************************\
# Removing the duplicate transactionids
#\***************************************************************************/
silver_df = bronze_df.dropDuplicates(["transaction_id"])
silver_df.count()

#/***************************************************************************\
# Checking the valid ship date
# Valid case: ship date should be greater than order date
#\***************************************************************************/
silver_df.filter(col("ship_date") < col("order_date")).show(5) 

#/***************************************************************************\
# Replacing invalid ship date with None
#\***************************************************************************/
silver_df = silver_df.withColumn("ship_date", when(col("ship_date") < col("order_date"), None).otherwise(col("ship_date")))

#/***************************************************************************\
# Checking valid values for quantity 
# Invalid case: quantity value <= zero
#\***************************************************************************/
silver_df.filter(col("quantity") <= 0).show(5)

#/***************************************************************************\
# Taking only the proper quantity value
#\***************************************************************************/
silver_df = silver_df.filter(col("quantity") > 0)

#/***************************************************************************\
# Checking valid values for unit price 
# Invalid case: unit price value <= zero
#\***************************************************************************/
silver_df.filter(col("unit_price") <= 0).show(5)

#/***************************************************************************\
# Taking only the proper unit price value
#\***************************************************************************/
silver_df = silver_df.withColumn("unit_price", when(col("unit_price") <= 0, None).otherwise(col("unit_price")))

#/***************************************************************************\
# Checking for invalid discount percentage
# Invalid case: (<0, >100)
#\***************************************************************************/
silver_df.filter((col("discount_percentage") > 100) | (col("discount_percentage") < 0)).show(5)

#/***************************************************************************\
# Replacing with None for invalid discount percentage
#\***************************************************************************/
silver_df = silver_df.withColumn("discount_percentage", when(col("discount_percentage") > 100, None). when(col("discount_percentage") < 0, None).otherwise(col("discount_percentage")))

#/***************************************************************************\
# Checking the valid customer age 
# Invalid case : (<15, >100)
#\***************************************************************************/
silver_df.filter((col("customer_age") < 15) | (col("customer_age") > 100)).show(5)

#/***************************************************************************\
# Replacing with None for invalid customer age
#\***************************************************************************/
silver_df = silver_df.withColumn("customer_age", when((col("customer_age") > 100) | (col("customer_age") < 0), None).otherwise(col("customer_age")))

#/***************************************************************************\
# Checking the gender column
#\***************************************************************************/
silver_df.groupBy("gender").count().show()

#/***************************************************************************\
# Replace the gender column correctly M -> Male, F->Female
#\***************************************************************************/
silver_df = silver_df.withColumn("gender", when(upper(col("gender")) == 'M', "MALE").when(upper(col("gender")) == 'F', "FEMALE").when(col("gender") == 'Male', "MALE").when(col("gender") == 'Female', "FEMALE").when(upper(col("gender")).isin("MALE","FEMALE"), col("gender")).otherwise(None))

#/***************************************************************************\
# checking the valid payment options 
# Invalid -> Crypto
#\***************************************************************************/
silver_df.filter(~col("payment_type").isin("Card", "UPI", "COD")).show(5)

#/***************************************************************************\
# replacing the invalid payment option as None
#\***************************************************************************/
silver_df = silver_df.withColumn("payment_type", when(col("payment_type").isin("Card", "UPI", "COD"), col("payment_type")).otherwise(None))

#/***************************************************************************\
# Writing the final data as parquet format (Silver Layer - cleaned data)
#\***************************************************************************/
silver_df.write.mode("overwrite").parquet("/opt/spark-data/transformed_data/silver/retail_sales_silver.parquet")