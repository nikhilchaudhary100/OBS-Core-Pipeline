import re

# CONCEPT 1: Pre-compile the regex pattern ONCE at the module level for maximum speed
LOG_PATTERN = re.compile(r"\[(.*?)\] \[(.*?)\] \[(.*?)\] (.*)")

def parse_log_line(line):
    # CONCEPT 2: The Safety Net (Graceful Degradation)
    try:
        # Use our pre-compiled pattern, which is much faster than re.search()
        match = LOG_PATTERN.search(line)
        
        if not match:
            # If the line is total gibberish and doesn't match our brackets, trigger an error
            raise ValueError("Corrupted line structure: Brackets not found")

        timestamp, log_level, sensor_id, metrics_string = match.groups()
        
        metrics_dict = {}
        
        # Step-by-step splitting of the metrics
        # Example: "Temp: 32C | PM2.5: 45ug/m3" -> ["Temp: 32C", "PM2.5: 45ug/m3"]
        metric_parts = metrics_string.split("|")
        
        for part in metric_parts:
            # Example: "Temp: 32C" -> key="Temp", value="32C"
            if ":" not in part:
                 raise ValueError(f"Malformed metric part: {part}")
                 
            key, value = part.split(":", 1)
            # Clean the whitespace immediately
            clean_key = key.strip()
            clean_value = value.strip()
            
            
            if not clean_value:
                raise ValueError(f"Missing data value for metric: {clean_key}")
                
            metrics_dict[clean_key] = clean_value
            
        # If we made it here, the data is perfect!
        return {
            "status": "success",
            "timestamp": timestamp,
            "level": log_level,
            "sensor": sensor_id,
            "metrics": metrics_dict
        }
        
    
    # We ONLY catch ValueError. This represents bad data from the sensors.
    except ValueError as e:
        return {
            "status": "error",
            "error_type": "DataFormatError",
            "error_message": str(e),
            "original_line": str(line).strip() 
        }