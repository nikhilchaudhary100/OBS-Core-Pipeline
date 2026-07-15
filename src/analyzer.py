#Write functions that loop through the parsed data to answer specific questions:
    #Q1) What was the average PM2.5 reading for SENSOR_42 between 3:00 PM and 5:00 PM?
    #Q2) Did any sensor record three consecutive readings of CO2 above a dangerous threshold of 800ppm?

from datetime import datetime

def analyze_logs(parsed_logs_stream):
    print("Starting Diagnostic Analytics...")
    
    # Trackers for Question 1
    pm25_total = 0
    pm25_count = 0
    
    # Trackers for Question 2
    co2_streaks = {}
    dangerous_co2_threshold = 800 # ppm
    alarms_triggered = []

    # Stream processing: We look at one log at a time!
    for log in parsed_logs_stream:

        # Skip logs that failed in the parser (our Dead Letter Queue handles these)
        if log["status"] == "error":
            continue
            
        sensor = log["sensor"]
        metrics = log["metrics"]
        
        # Question 1: Average PM2.5 for SENSOR_42 (14:00 to 16:00) ---
        if sensor == "SENSOR_42" and "PM2.5" in metrics:
            # Convert the string timestamp into a Python datetime object
            log_time = datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S")
            
            # Check if the hour is 14 or 15 (which covers 2:00 PM to 3:59 PM)
            if 15 <= log_time.hour < 17:
                # Clean the 'ug/m3' off the value to get the raw number
                try:
                    pm25_val = int(metrics["PM2.5"].replace('ug/m3', ''))
                    pm25_total += pm25_val
                    pm25_count += 1
                except ValueError:
                    pass # Ignore gracefully if the value is corrupted
                    
        # Question 2: Three consecutive CO2 readings above threshold ---
        if "CO2" in metrics:
            try:
                co2_val = int(metrics["CO2"].replace('ppm', ''))
                
                if co2_val > dangerous_co2_threshold:
                    # Increase the streak for this specific sensor!
                    co2_streaks[sensor] = co2_streaks.get(sensor, 0) + 1
                    
                    if co2_streaks[sensor] >= 3:
                        alarms_triggered.append(f"🚨 ALARM! {sensor} hit 3 consecutive dangerous CO2 levels at {log['timestamp']}!")
                        # Reset streak so we don't spam the alarm every second after
                        co2_streaks[sensor] = 0
                else:
                    # Normal reading, reset the streak!
                    co2_streaks[sensor] = 0
                    
            except ValueError:
                # If it's corrupted gibberish, reset the streak just to be safe
                co2_streaks[sensor] = 0

    # Calculate final average safely (prevent dividing by zero!)
    avg_pm25 = (pm25_total / pm25_count) if pm25_count > 0 else 0
    
    return avg_pm25, alarms_triggered