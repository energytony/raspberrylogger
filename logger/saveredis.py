from timeloop import Timeloop
from datetime import timedelta
import redis
import csv
import json
import os
from datetime import datetime
base_directory = "/home/tonyho/data"
tl = Timeloop()

@tl.job(interval=timedelta(seconds=600))  # Change to timedelta(hours=6) for every 6 hours
def fetch_and_save_redis_data():
    # Connect to Redis
    r = redis.StrictRedis(host="127.0.0.1", port="6379", charset="utf-8", decode_responses=True, password="innovura_d84ser4xyz", db=0)

    # Read the last length of the Redis list (if available)
    last_length = int(r.get('last_processed_length') or 0)
    
    max_length = r.llen('raspberry')

    print (" max : "+ str(max_length) + " last_length : "+ str(last_length))
    # Retrieve new data from Redis starting from the last length
    data_list = r.lrange('raspberry', 0, max_length-last_length)

    if data_list:
        # Update last processed length in Redis
        r.set('last_processed_length', max_length)

        # Process and categorize data by date
        dated_data = {}
        for data in data_list:
            try:
                parsed_data = json.loads(data)
                if isinstance(parsed_data, dict):
                    date_str = datetime.strptime(parsed_data['time'], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d")
                    dated_data.setdefault(date_str, []).append(parsed_data)
            except json.JSONDecodeError:
                print(f"Skipping item, not valid JSON: {data}")

        # Write data to corresponding CSV files
        for date_str, entries in dated_data.items():
            csv_file = os.path.join(base_directory, f"{date_str}.csv")

            
            # Check if file exists and read existing data if it does
            existing_data = []
            if os.path.isfile(csv_file):
                with open(csv_file, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    existing_data = [row for row in reader]

            # Combine new and existing data
            combined_data = entries + existing_data

            # Write combined data to CSV
            if combined_data:
                csv_columns = set(combined_data[0].keys())
                try:
                    with open(csv_file, 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                        writer.writeheader()
                        for data in combined_data:
                            if set(data.keys()) == csv_columns:
                                writer.writerow(data)
                        print(f"Data saved to {csv_file} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                except IOError:
                    print("I/O error")
    else:
        print("No new valid JSON data found.")

if __name__ == "__main__":
    print("Save Program starting...")
    tl.start(block=True)
