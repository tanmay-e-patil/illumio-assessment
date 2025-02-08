from typing import List, Dict
from collections import defaultdict
import csv

def read_flow_logs(log_file: str) -> str:  
    with open(log_file, "r") as file:
        content = file.read()
    return content

def preprocess_logs(content: str) -> List[str]:
    lines = content.split("\n")
    processed_lines = [l.strip() for l in lines]
    return processed_lines

def parse_logs(logs: List[str]):
    pass

def get_protocol_map(csv_path: str) -> Dict[str, str]:
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
            dest_port = row[0].strip()
            protocol_name = row[1].strip().lower()
            tag = row[2].strip()
            lookup_table[(dest_port, protocol_name)] = tag
    return lookup_table



    

if __name__ == "__main__":
    content = read_flow_logs("./data/input/flow_logs.txt")
    lines = preprocess_logs(content=content)
    protocol_map = get_protocol_map("./data/protocol_map/protocol-numbers.csv")
    lookup_table = fetch_lookup_table("./data/input/lookup_table.csv")
    tag_count = defaultdict(int)
    count = defaultdict(int)


    for line in lines:
        fields = line.split()
        if fields[0] != '2':
            print("Version not supported")
            continue
        dest_port, protocol_number = fields[6],fields[7]
        
        if dest_port == '-' or protocol_number == '-':
            continue
        protocol_name = protocol_map[protocol_number]
        if (dest_port, protocol_name) in lookup_table:
            tag_count[lookup_table[(dest_port, protocol_name)]] += 1
        else:
            tag_count['Untagged'] += 1
        count[(dest_port, protocol_name)] += 1

        

    for t,v in sorted(tag_count.items()):
        print(t,v)   
    print()

    for k,v in sorted(count.items()):
        d,p = k
        print(d,p,v)          
