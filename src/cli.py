import argparse
import time
from src.parser import parse_log_line
from src.error_handler import log_to_dlq
from src.analyzer import analyze_logs

def stream_and_filter_logs(file_path):
    """
    Reads the raw log file line-by-line:
    - Routes corrupted logs directly to disk via log_to_dlq()
    - Yields clean parsed dictionaries to the analyzer stream
    """
    with open(file_path, "r") as log_file:
        for line in log_file:
            result = parse_log_line(line)
            if result["status"] == "error":
                log_to_dlq(result)
            else:
                yield result


def main():
    # 1. Set up the Argument Parser
    parser = argparse.ArgumentParser(description="Observability Core Pipeline CLI")
    
    # 2. Add our specific commands
    parser.add_argument("--file", required=True, help="Path to the raw log file")
    parser.add_argument("--detect-spikes", action="store_true", help="Run the diagnostic analyzer to find spikes")
    parser.add_argument("--sensor", type=str, default="SENSOR_42", help="Specific sensor ID to analyze")
    
    # 3. Parse the commands the user actually typed in the terminal
    args = parser.parse_args()
    
    print(f"Initializing Observability Pipeline...")
    print(f"Target File: {args.file}")
    
    # Start the stopwatch
    start_time = time.time()
    
    # Bridge to the Core Engine (This is where we connect the dots)
    if args.detect_spikes:
        print(f"Spike detection activated for {args.sensor}...")

        # Create generator stream (routes errors to DLQ, yields clean logs)
        clean_stream = stream_and_filter_logs(args.file)

        # Stream directly into analyzer
        avg_pm25, alarms = analyze_logs(clean_stream)
        
    print("\n📊 --- Analytics Results ---")
    print(f"Average PM2.5 for {args.sensor}: {avg_pm25:.2f}")
    print(f"Alarms Triggered ({len(alarms)}):")
    for alarm in alarms:
        print(f"  {alarm}")

    # 6. Stop the stopwatch
    end_time = time.time()
    
    print(f"Pipeline execution finished perfectly!")
    print(f"Total Execution Time: {end_time - start_time:.4f} seconds")

# This ensures the CLI logic runs when we execute the file from the terminal
if __name__ == "__main__":
    main()