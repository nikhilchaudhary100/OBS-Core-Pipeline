import json
import os

# CONCEPT 1: Define the exact path to our physical hard drive reject bin
DLQ_FILE_PATH = "data/dead_letters/dlq.json"

def log_to_dlq(error_record):
    """
    Takes the error dictionary from the parser and permanently saves it to disk.
    Appends records as JSON Lines (.jsonl format).
    """
    # 1. Ensure the target directory exists on disk (prevents FileNotFoundError)
    directory = os.path.dirname(DLQ_FILE_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    # CONCEPT 2: We open the file in 'a' (append) mode. 
    # If we used 'w' (write) mode, it would delete the old errors every time!
    # 'a' ensures we just add the new broken part to the bottom of the bin.
    with open(DLQ_FILE_PATH, 'a') as dlq_file:
        
        # Convert the Python dictionary into a JSON string
        json_string = json.dumps(error_record)
        
        # Write it to the file, and add a newline (\n) so the next error goes below it
        dlq_file.write(json_string + '\n')