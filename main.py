from typing import List, Dict
from collections import defaultdict
import csv
import argparse
import os

def read_flow_logs(log_filepath: str) -> str:  
    with open(log_filepath, "r") as file:
        log_data = file.read()
    return preprocess_logs(log_data)

def preprocess_logs(log_data: str) -> List[str]:
    log_entries = log_data.split("\n")
    cleaned_logs = [entry.strip() for entry in log_entries]
    return cleaned_logs

def fetch_protocol_map(csv_path: str) -> Dict[str, str]:   
    protocols = {}
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row and len(row) >= 2 and row[0].strip() and row[1].strip():
                protocol_number = row[0].strip()
                protocol_name = row[1].strip().lower()
                protocols[protocol_number] = protocol_name
    return protocols

def fetch_lookup_table(csv_path: str) -> Dict[tuple, str]:
    lookup_table = {}
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row and len(row) == 3:
                dest_port, protocol_name, tag = row
                lookup_table[(dest_port.strip(), protocol_name.strip().lower())] = tag.strip()
            else:
                exit("Invalid lookup table format")
    return lookup_table

def process_log_entries(log_entries: List[str], lookup_table: Dict[tuple, str], protocol_map: Dict[str, str]) -> tuple[Dict[str, int], Dict[tuple, int]]:
    tag_counts = defaultdict(int)
    port_protocol_count = defaultdict(int)

    for log in log_entries:
        fields = log.split()
        if len(fields) < 8 or fields[0] != '2':
            continue       
        dest_port, protocol_number = fields[6],fields[7]
        
        if dest_port == '-' or protocol_number == '-':
            continue
       
        protocol_name = protocol_map[protocol_number] 
        tag = lookup_table.get((dest_port, protocol_name), "Untagged")
        tag_counts[tag] += 1
        port_protocol_count[(dest_port, protocol_name)] += 1
    
    return tag_counts, port_protocol_count

def write_output(output_filepath: str, tag_count: Dict[str, int], port_protocol_count: Dict[tuple, int]):
    with open(output_filepath, "w") as file:
        file.write("Tag Counts:\n")
        file.write("Tag,Count\n")
        for tag, count in tag_count.items():
            file.write(f"{tag},{count}\n")
        
        file.write("\nPort/Protocol Combination Counts:\n")
        file.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_count.items():
            file.write(f"{port},{protocol},{count}\n")

def main():
    PROTOCOL_MAP_FILEPATH = "./data/protocol_map/protocol-numbers.csv"

    parser = argparse.ArgumentParser(description="Process VPC flow logs.")
    parser.add_argument("--flow-logs", required=True, help="Path to the flow logs file")
    parser.add_argument("--lookup-table", required=True, help="Path to the lookup table CSV file")
    parser.add_argument("--output-file", required=True, help="Path to the output file")
    
    args = parser.parse_args()

    if not os.path.exists(args.flow_logs):
        exit(f"Error: The file {args.flow_logs} does not exist.")
    if not os.path.exists(args.lookup_table):
        exit(f"Error: The file {args.lookup_table} does not exist.")
    if not os.path.isdir(os.path.dirname(args.output_file)):
        exit(f"Error: The directory for the output file {args.output_file} does not exist.")

    log_entries = read_flow_logs(args.flow_logs)
    lookup_table = fetch_lookup_table(args.lookup_table)
    protocol_map = fetch_protocol_map(PROTOCOL_MAP_FILEPATH)    

    tag_counts, port_protocol_count = process_log_entries(log_entries, lookup_table, protocol_map)
   
    write_output(args.output_file, tag_counts, port_protocol_count)


if __name__ == "__main__":
    main()
    