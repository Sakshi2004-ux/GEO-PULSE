
import pandas as pd
from pathlib import Path

# Locate the project root directory
project_root = Path(__file__).resolve().parents[2]

# Locate the raw GPS dataset
dataset_path = project_root / "data" / "raw" / "gps_pings.csv"

# Load the dataset
df = pd.read_csv(dataset_path)

print("GEOPULSE DATASET VALIDATION")
print("---------------------------")

print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Records:")
print(df.head())

print("\nColumn Information:")
print(df.info())


# ==========================================
# DATA QUALITY VALIDATION
# ==========================================

# 1. Check missing values
print("\n1. MISSING VALUES")
print(df.isnull().sum())


# 2. Check duplicate complete records
print("\n2. DUPLICATE ROWS")
print("Duplicate rows:", df.duplicated().sum())


# 3. Check duplicate device observations
print("\n3. DUPLICATE DEVICE-TIMESTAMP PAIRS")
print(
    df.duplicated(
        subset=["DeviceID", "Timestamp"]
    ).sum()
)


# 4. Check latitude and longitude ranges
print("\n4. COORDINATE RANGES")

print("Minimum Latitude:", df["Lat"].min())
print("Maximum Latitude:", df["Lat"].max())

print("Minimum Longitude:", df["Long"].min())
print("Maximum Longitude:", df["Long"].max())


# 5. Check unique devices
print("\n5. UNIQUE DEVICES")
print("Total Devices:", df["DeviceID"].nunique())


# 6. Check GPS records per device
print("\n6. RECORDS PER DEVICE")

records_per_device = df.groupby("DeviceID").size()

print(records_per_device.describe())

print(
    "Devices with unexpected record counts:",
    (records_per_device != 50).sum()
)


# 7. Check records per day
print("\n7. RECORDS PER DAY")

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

print(
    df.groupby(df["Timestamp"].dt.date).size()
)


# 8. Check activity distribution
print("\n8. ACTIVITY DISTRIBUTION")

print(df["Activity"].value_counts())
