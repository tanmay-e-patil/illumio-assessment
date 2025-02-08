# Illumio Assessment
The program processes AWS VPC Flow Logs (Version 2 only) to generate statistics on port and protocol usage. It first reads the flow log file and preprocesses it by cleaning and splitting the entries. It then loads a protocol mapping file (protocol-numbers.csv) to convert protocol numbers into human-readable names and a lookup table (lookup-table.csv) to associate port-protocol pairs with tags. Each log entry is then processed to extract the destination port and protocol, checking for missing or unsupported values. The program increments counts for both recognized tags and unmatched entries. Finally, the results, including tag counts and port/protocol combination counts, are written to an output file in .txt format.

## Assumptions
* Only v2 logs are supported.
* If a log does not have a destination port or protocol, then that log should be skipped.
* Output needs to be in a single .txt file.
* Protocol numbers must exist in protocol-numbers.csv; otherwise, they are labeled as "unknown."
* Store the tag and protocol name in lowercase in the result file to make matches case insensitive.

## How to run

### Usage
```
usage: main.py [-h] --flow-logs FLOW_LOGS --lookup-table LOOKUP_TABLE --output-file OUTPUT_FILE

Process VPC flow logs.

options:
  -h, --help            show this help message and exit
  --flow-logs FLOW_LOGS
                        Path to the flow logs file
  --lookup-table LOOKUP_TABLE
                        Path to the lookup table CSV file
  --output-file OUTPUT_FILE
                        Path to the output file
```

### Example
```
python3 main.py --flow-logs ./data/input/flow_logs.txt --lookup-table ./data/input/lookup_table.csv --output-file ./output.txt
```


## Testing
Tested manually with:
* Cases with incorrect CLI arguments.
* Cases with case-sensitive values, e.g., entries with sv_p1 and sv_P1 tags in lookup.csv.
* Cases where destination and protocol number are of value '-'.
* Cases where the flow log is malformed.