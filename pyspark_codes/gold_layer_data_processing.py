"""
File Name: gold_layer_processing.py

Description:
    This PySpark file is used for Gold layer data processing.
    It performs business-level transformations and creates
    aggregated datasets that are ready for reporting and analytics.

Processing:
    -> Reads refined data from the Silver layer.
    -> Applies business logic and KPI calculations.
    -> Creates aggregated business-purpose datasets.
    -> Generates optimized data outputs for dashboards and reporting.

Business Purpose Outputs:
    1. Daily Sales Value
       => Provides total sales value aggregated on a daily basis.

    2. Product Category Wise Sales Value
       => Provides sales value analysis based on product categories.

    3. City Wise Sales Value
       => Provides sales value insights based on city-level aggregation.

Layer:
    Gold Layer (Business Ready Data)
"""

#/***************************************************************************\
# Required Headers
#\***************************************************************************/
from pyspark.sql.functions import *

#/***************************************************************************\
# Data Reading from silver layer parquet file
#\***************************************************************************/
silver_df = spark.read.parquet("/opt/spark-data/transformed_data/silver/retail_sales_silver.parquet")

# -----------------------------------------------------------------------------
# DATA TRANSFORMATION FOR BUSINESS PURPOSE
# -----------------------------------------------------------------------------

#/***************************************************************************\
# Calculating the total amount (new column) and storing it in gold_df
#\***************************************************************************/
gold_df = silver_df.withColumn("total_amount", round(col("quantity") * col("unit_price") * (1-col("discount_percentage")/100),2))

# -----------------------------------------------------------------------------
# BUSINESS PURPOSE DATA 1 - Daily Sales Value
# -----------------------------------------------------------------------------
#/***************************************************************************\
# Calculating the daily sale values
#\***************************************************************************/
daily_sale_df = gold_df.groupBy("order_date").agg(round(sum("total_amount"), 2).alias("total_revenue"), round(count("transaction_id")).alias("total_orders"), round(avg("total_amount"), 2).alias("avg_order_value"))

#/***************************************************************************\
# Writing the calculated daily sale values as parquet file (gold layer output 1) 
#\***************************************************************************/
daily_sale_df.write.mode("overwrite").parquet("/opt/spark-data/transformed_data/gold/daily_sales_metrics.parquet")

# -----------------------------------------------------------------------------
#  BUSINESS PURPOSE DATA 2 - Product Category wise Sale Value
# -----------------------------------------------------------------------------
#/***************************************************************************\
# Calculating the product wise values
#\***************************************************************************/
product_perf_df = gold_df.groupBy("product_category").agg(round(sum("total_amount"), 2).alias("product_category_total_revenue"), sum("quantity").alias("product_units_sold"), count("transaction_id").alias("total_product_orders"))

#/***************************************************************************\
# writing the calculated product performance values as parquet file (gold layer output 2)
#\***************************************************************************/
product_perf_df.write.mode("overwrite").parquet("/opt/spark-data/transformed_data/gold/product_performance_metrics.parquet")

# -----------------------------------------------------------------------------
#  BUSINESS PURPOSE DATA 3 - City wise Sales Value
# -----------------------------------------------------------------------------
#/***************************************************************************\
# Calculating the city wise sale value
#\***************************************************************************/
city_sale_df = gold_df.groupBy("city", "state").agg(round(sum("total_amount"), 2).alias("city_total_revenue"), round(count("transaction_id")).alias("city_total_orders"), round(avg("total_amount"), 2).alias("city_avg_order_value"))

#/***************************************************************************\
# Writing the calculated city sale values as parquet file (gold layer output 3)
#\***************************************************************************/
city_sale_df.write.mode("overwrite").parquet("/opt/spark-data/transformed_data/gold/city_sales_metrics.parquet")