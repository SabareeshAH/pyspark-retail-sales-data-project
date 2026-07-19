# ==========================================================
# Required Headers
# ==========================================================
import csv
import random
from datetime import datetime, timedelta
import os

# ==========================================================
# Configuration
# ==========================================================

# Get the current working directory
BASE_DIR = os.getcwd()

# Output directory for the generated CSV file
OUTPUT_DIR = os.path.join(BASE_DIR, "data/raw")

# Output file name
OUTPUT_FILE = "retail_sales_raw.csv"

# Total number of records to generate
NUM_RECORDS = 250000

# Create the output directory if it does not exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Complete path of the output CSV file
file_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

# ==========================================================
# Reference Data
# ==========================================================

# List of major Indian cities and their corresponding states
cities = [
    ("Mumbai", "Maharashtra"),
    ("Delhi", "Delhi"),
    ("Bengaluru", "Karnataka"),
    ("Hyderabad", "Telangana"),
    ("Chennai", "Tamil Nadu"),
    ("Kolkata", "West Bengal"),
    ("Pune", "Maharashtra"),
    ("Ahmedabad", "Gujarat"),
    ("Jaipur", "Rajasthan"),
    ("Tiruchirapalli", "Tamil Nadu"),
    ("Indore", "Madhya Pradesh"),
    ("Visakhapatnam", "Andhra Pradesh"),
    ("Coimbatore", "Tamil Nadu"),
    ("Kochi", "Kerala")
]

# Product categories with their respective price ranges
categories = {
    "Electronics": (100, 2000),
    "Fashion": (20, 500),
    "Grocery": (1, 50),
    "Furniture": (50, 1500),
    "Sports": (10, 800)
}

# Possible payment methods (includes missing values)
payment_types = ["Card", "UPI", "COD", "Crypto", None]

# Different gender representations (includes missing values)
genders = ["M", "F", "Male", "Female", None]

# Possible order statuses
order_statuses = ["Delivered", "Cancelled", "Returned"]

# Date range for order generation
start_date = datetime(2023, 1, 1)
end_date = datetime(2026, 1, 1)

# ==========================================================
# Helper Function
# ==========================================================

def random_date(start, end):
    """
    Generate a random date between the given start and end dates.
    """
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# ==========================================================
# Data Generation
# ==========================================================

# Open CSV file in write mode
with open(file_path, mode="w", newline="", encoding="utf-8") as file:

    # Create CSV writer object
    writer = csv.writer(file)

    # Write column headers
    writer.writerow([
        "transaction_id",
        "order_date",
        "ship_date",
        "customer_id",
        "customer_age",
        "gender",
        "product_id",
        "product_category",
        "quantity",
        "unit_price",
        "discount_percentage",
        "city",
        "state",
        "payment_type",
        "order_status",
        "ingestion_date"
    ])

    # Generate the required number of records
    for i in range(NUM_RECORDS):

        # Generate duplicate transaction IDs intentionally
        transaction_id = random.randint(1, NUM_RECORDS // 2)

        # Random order date
        order_date = random_date(start_date, end_date)

        # Ship date may be before the order date to simulate bad data
        ship_date = order_date + timedelta(days=random.randint(-3, 10))

        # Customer information
        customer_id = f"CUST{random.randint(1, 100000)}"

        # Generate valid, invalid and missing customer ages
        customer_age = random.choice([
            random.randint(18, 70),      # Valid
            random.randint(-10, 10),     # Invalid
            random.randint(120, 200),    # Unrealistic
            None                         # Missing
        ])

        # Random gender value
        gender = random.choice(genders)

        # Select a product category
        category = random.choice(list(categories.keys()))

        # Retrieve price range for the selected category
        price_min, price_max = categories[category]

        # Generate valid, negative and missing prices
        unit_price = random.choice([
            round(random.uniform(price_min, price_max), 2),
            -random.uniform(1, 100),
            None
        ])

        # Generate valid, zero and negative quantities
        quantity = random.choice([
            random.randint(1, 10),
            0,
            -random.randint(1, 5)
        ])

        # Generate valid, invalid and missing discount percentages
        discount_percentage = random.choice([
            round(random.uniform(0, 50), 2),
            round(random.uniform(60, 150), 2),
            None
        ])

        # Select a random city and state
        city, state = random.choice(cities)

        # Write the generated record into the CSV file
        writer.writerow([
            transaction_id,
            order_date.strftime("%Y-%m-%d"),
            ship_date.strftime("%Y-%m-%d"),
            customer_id,
            customer_age,
            gender,
            f"PROD{random.randint(1, 50000)}",
            category,
            quantity,
            unit_price,
            discount_percentage,
            city,
            state,
            random.choice(payment_types),
            random.choice(order_statuses),
            datetime.now().strftime("%Y-%m-%d")
        ])

# ==========================================================
# Completion Message
# ==========================================================

print(f"Generated {NUM_RECORDS} records at:\n{file_path}")