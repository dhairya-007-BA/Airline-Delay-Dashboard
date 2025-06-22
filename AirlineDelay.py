import pandas as pd

# === STEP 1: Load sample from Excel file ===
file_path = "/Users/dhairyasinghal/Desktop/Project/Personal Projects/Airline_Delay_Cause.xlsx"

# Read first 1000 rows to avoid memory overload
df = pd.read_excel(file_path, sheet_name="Main Datset", nrows=1000)

# Clean and normalize column names
df.columns = df.columns.str.strip()

# === STEP 2: Filter out rows with no flight activity ===
df = df[df["ARR Flights"].notnull() & (df["ARR Flights"] > 0)]

# === STEP 3: Feature Engineering ===
df["DelayRate"] = (df["ARR Del 15"] / df["ARR Flights"]) * 100
df["IsDelayed"] = df["DelayRate"].apply(lambda x: 1 if x > 20 else 0)
df["MonthName"] = pd.to_datetime(df["Month"], format="%m").dt.month_name()

def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"

df["Season"] = df["Month"].apply(get_season)

# === STEP 4: Select Relevant Columns for Tableau ===
selected_columns = [
    "Year", "Month", "MonthName", "Season",
    "Carrier", "Carrier Name", "Airport", "Airport Name",
    "ARR Flights", "ARR Del 15", "ARR Delay", "ARR Cancelled",
    "Carrier Delay", "Weather Delay", "Nas Delay", "Security Delay", "Late Aircraft Delay",
    "DelayRate", "IsDelayed"
]

# Use only available columns (safe for missing ones)
final_df = df[[col for col in selected_columns if col in df.columns]]

# === STEP 5: Export cleaned data to CSV for Tableau ===
output_path = "/Users/dhairyasinghal/Desktop/Project/Flight_Delay_Sample.csv"
final_df.to_csv(output_path, index=False)

print("Exported cleaned data to:", output_path)

