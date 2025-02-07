from typing import List
def read_flow_logs(log_file: str) -> str:  
    with open(log_file, "r") as file:
        content = file.read()
    return content

def preprocess_logs(content: str) -> List[str]:
    lines = content.split("\n")
    processed_lines = [l.strip() for l in lines]
    return processed_lines

# def parse_logs(logs: List[str]) -> 
    
    

if __name__ == "__main__":
    content = read_flow_logs("./data/input/flow_logs.txt")
    lines = preprocess_logs(content=content)
    for line in lines:
        print(line.split())
