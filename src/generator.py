import random
import time
from datetime import datetime, timedelta
import os

def generate_logs(num_lines=10000, output_file="data/raw_logs/sensor_data.log"):
    # Ensure our data directory exists (Lego bins!)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    sensors = ["SENSOR_42", "SENSOR_07", "SENSOR_99", "SENSOR_15"]
    
    # We will simulate data starting from this exact time
    current_time = datetime(2026, 6, 20, 14, 32, 1)

    print(f"Generating {num_lines} logs of pure chaos...")
    
    with open(output_file, 'w') as f:
        for _ in range(num_lines):
            # 1. Generate base healthy data
            sensor = random.choice(sensors)
            temp = random.randint(20, 40)
            pm25 = random.randint(10, 50)
            co2 = random.randint(350, 450)
            log_level = "INFO"
            
            # 2. Roll the dice for Chaos! (1-100)
            chaos_roll = random.randint(1, 100)
            
            # Inject an Anomaly (5% chance) - Crazy high pollution!
            if chaos_roll <= 5:
                pm25 = random.randint(250, 500)
                log_level = "WARN"
                
            # Inject a Missing Data Error (3% chance) - Dropped the Temp!
            elif chaos_roll <= 8:
                temp = ""  
                
            # Inject a Corrupted String Error (2% chance) - Total gibberish!
            elif chaos_roll <= 10:
                co2 = "ERR_#$@%^"
                log_level = "ERROR"

            # 3. Format the log line
            # E.g., [2026-06-20 14:32:01] [INFO] [SENSOR_42] Temp: 32C | PM2.5: 45ug/m3 | CO2: 400ppm
            # If temp is missing, it will look like Temp: C, which our parser will have to handle!
            log_line = f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] [{log_level}] [{sensor}] Temp: {temp}C | PM2.5: {pm25}ug/m3 | CO2: {co2}ppm\n"
            
            # 4. Write it to our file
            f.write(log_line)
            
            # Move time forward by 1 second for the next log
            current_time += timedelta(seconds=1)

    print(f"Done! Created {num_lines} logs at {output_file}")

# This ensures the script runs when we execute it from the terminal
if __name__ == "__main__":
    generate_logs()