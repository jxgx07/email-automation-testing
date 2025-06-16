import os
import sys
import json
import pandas as pd
from datetime import datetime, timedelta

# Get timestamp from Jenkins argument or default for local test
timestamp = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

payload_dir = "payloads"
time_window = timedelta(hours=24)
now = datetime.now()

files = []
for fname in os.listdir(payload_dir):
    if fname.startswith("payload_") and fname.endswith(".json"):
        file_path = os.path.join(payload_dir, fname)
        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
        if now - file_mtime <= time_window:
            files.append(file_path)

records = []
for file_path in files:
    with open(file_path, 'r') as f:
        try:
            payload = json.loads(f.read())
            for from_email, to_emails in payload.items():
                for to_email in to_emails:
                    records.append({"From Email": from_email, "To Email": to_email})
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON file: {file_path}")

df = pd.DataFrame(records)

if df.empty:
    print("No valid payloads found in last 24 hours.")
    sys.exit(0)

for file in os.listdir():
    if file.startswith("slave") and file.endswith(".xlsx"):
        os.remove(file)

half = len(df) // 2
df_slave1 = df.iloc[:half]
df_slave2 = df.iloc[half:]

df_slave1.to_excel(f"slave1_{timestamp}.xlsx", index=False)
df_slave2.to_excel(f"slave2_{timestamp}.xlsx", index=False)

print("Aggregation and splitting completed successfully.")
