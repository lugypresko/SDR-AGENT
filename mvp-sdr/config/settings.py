"""
CONFIG: settings.py

PURPOSE:
Central configuration for the SDR pipeline.

SETTINGS:
- THRESHOLDS:
  - fallback_threshold (float): Max allowed % of leads hitting fallback before alert.
  - minimum_unique_pains (int): Min number of distinct pains required in a batch.
  
- PATHS:
  - input_csv_path (str): Default path to leads.csv
  - output_csv_path (str): Default path to generated_emails.csv
  - metrics_store_path (str): Path to metrics.json
  
- LOGGING:
  - log_level (str): "INFO", "DEBUG", "WARN"
  - log_file (str): Path to pipeline.log
"""

# Placeholders
FALLBACK_THRESHOLD = 0.1
MINIMUM_UNIQUE_PAINS = 3
INPUT_CSV_PATH = "leads.csv"
OUTPUT_CSV_PATH = "generated_emails.csv"
LOG_LEVEL = "INFO"
