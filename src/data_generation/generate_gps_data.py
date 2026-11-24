
import pandas as pd
import numpy as np
from pathlib import Path

# ==========================================
# 1. CONFIGURATION
# ==========================================

NUM_DEVICES = 200
NUM_DAYS = 5
RANDOM_SEED = 42

rng = np.random.default_rng(RANDOM_SEED)

START_DATE = "2026-11-16"


# ==========================================
# 2. SIMULATED MUMBAI ZONES
# ==========================================

zones = {
    "Andheri": (19.1197, 72.8468),
    "Bandra": (19.0596, 72.8295),
    "BKC": (19.0668, 72.8656),
    "Lower_Parel": (18.9977, 72.8376),
    "Powai": (19.1176, 72.9060),
    "Dadar": (19.0178, 72.8478)
}

residential_zones = [
    "Andheri", "Bandra", "Powai", "Dadar"
]

work_zones = [
    "BKC", "Lower_Parel", "Andheri", "Powai"
]

retail_zones = [
    "Bandra", "Lower_Parel", "Dadar", "Andheri"
]


# ==========================================
# 3. GPS OBSERVATION TIMES
# ==========================================

observation_times = [
    "07:00",
    "08:00",
    "09:00",
    "12:30",
    "14:00",
    "17:30",
    "18:00",
    "19:00",
    "20:00",
    "21:00"
]


# ==========================================
# 4. INTERPOLATION FUNCTION
# ==========================================

def interpolate_location(start, end, progress):

    latitude = (
        start[0] + (end[0] - start[0]) * progress
    )

    longitude = (
        start[1] + (end[1] - start[1]) * progress
    )

    # Add small random GPS variation
    latitude += rng.normal(0, 0.0003)
    longitude += rng.normal(0, 0.0003)

    return latitude, longitude


# ==========================================
# 5. GENERATE DEVICE MOVEMENT
# ==========================================

records = []

for device_num in range(1, NUM_DEVICES + 1):

    device_id = f"DEV{device_num:04d}"

    # Assign different zones to each device
    home_zone = rng.choice(residential_zones)

    available_work_zones = [
        zone for zone in work_zones
        if zone != home_zone
    ]

    work_zone = rng.choice(available_work_zones)

    available_retail_zones = [
        zone for zone in retail_zones
        if zone != work_zone
    ]

    retail_zone = rng.choice(available_retail_zones)

    home = zones[home_zone]
    work = zones[work_zone]
    retail = zones[retail_zone]

    for day in range(NUM_DAYS):

        current_date = (
            pd.Timestamp(START_DATE)
            + pd.Timedelta(days=day)
        )

        # Daily movement anchor points
        anchors = [
            ("07:00", home, "Home", "Residential"),
            ("09:00", work, "Work", "Workplace"),
            ("14:00", work, "Work", "Workplace"),
            ("19:00", retail, "Retail", "Retail"),
            ("21:00", home, "Home", "Residential")
        ]

        anchor_times = [
            pd.Timestamp(f"{current_date.date()} {time}")
            for time, _, _, _ in anchors
        ]

        for time in observation_times:

            timestamp = pd.Timestamp(
                f"{current_date.date()} {time}"
            )

            # Find the surrounding anchor points
            segment = 0

            while (
                segment < len(anchor_times) - 2
                and timestamp > anchor_times[segment + 1]
            ):
                segment += 1

            start_time = anchor_times[segment]
            end_time = anchor_times[segment + 1]

            start_location = anchors[segment][1]
            end_location = anchors[segment + 1][1]

            # Calculate movement progress
            duration = (
                end_time - start_time
            ).total_seconds()

            elapsed = (
                timestamp - start_time
            ).total_seconds()

            progress = elapsed / duration

            # Generate interpolated GPS coordinates
            latitude, longitude = interpolate_location(
                start_location,
                end_location,
                progress
            )

            # Assign simulated activity
            if timestamp == anchor_times[0]:

                activity = "Home"
                current_zone = home_zone

            elif timestamp < anchor_times[1]:

                activity = "Commuting"
                current_zone = "In_Transit"

            elif timestamp <= anchor_times[2]:

                activity = "Work"
                current_zone = work_zone

            elif timestamp < anchor_times[3]:

                activity = "Commuting"
                current_zone = "In_Transit"

            elif timestamp == anchor_times[3]:

                activity = "Shopping"
                current_zone = retail_zone

            elif timestamp < anchor_times[4]:

                activity = "Commuting"
                current_zone = "In_Transit"

            else:

                activity = "Home"
                current_zone = home_zone

            # Store the generated GPS record
            records.append({
                "DeviceID": device_id,
                "Lat": latitude,
                "Long": longitude,
                "Timestamp": timestamp,
                "Zone": current_zone,
                "Activity": activity
            })


# ==========================================
# 6. CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(records)

df = df.sort_values(
    ["DeviceID", "Timestamp"]
).reset_index(drop=True)


# ==========================================
# 7. SAVE DATASET
# ==========================================

project_root = Path(__file__).resolve().parents[2]

output_folder = project_root / "data" / "raw"

output_folder.mkdir(
    parents=True,
    exist_ok=True
)

output_file = output_folder / "gps_pings.csv"

df.to_csv(output_file, index=False)


# ==========================================
# 8. DISPLAY RESULTS
# ==========================================

print("GEOPULSE GPS DATA GENERATED!")

print("\nDataset Shape:", df.shape)

print("\nFirst 5 Records:")
print(df.head())

print("\nUnique Devices:", df["DeviceID"].nunique())

print("\nTotal GPS Pings:", len(df))

print("\nMissing Values:")
print(df.isnull().sum())

print("\nActivity Distribution:")
print(df["Activity"].value_counts())

print("\nTimestamp Range:")
print(df["Timestamp"].min())
print(df["Timestamp"].max())

print("\nDataset saved at:", output_file)
