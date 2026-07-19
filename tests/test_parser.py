import pytest
# We import the Lego block that we want to test
from src.parser import parse_log_line

def test_valid_log_parsing():
    # 1. The Setup (Provide a perfect log)
    good_log = "[2026-06-20 14:32:01] [INFO] [SENSOR_42] Temp: 32C | PM2.5: 45ug/m3"
    
    # 2. The Action
    result = parse_log_line(good_log)
    
    # 3. The Assertions (Demand the truth!)
    assert result["status"] == "success"
    assert result["sensor"] == "SENSOR_42"
    assert result["metrics"]["Temp"] == "32C"

def test_corrupted_log_graceful_failure():
    # 1. The Setup (Provide absolute chaos - no brackets, missing data!)
    bad_log = "TOTAL GIBBERISH SENSOR_ERROR Temp:"
    
    # 2. The Action (Run our engine)
    result = parse_log_line(bad_log)
    
    # 3. The Assertions (Demand that it caught the error for our DLQ, and didn't crash!)
    assert result["status"] == "error"
    # We prove that it saved the original broken message so we can fix it later
    assert "original_line" in result 
    assert result["original_line"] == bad_log.strip()