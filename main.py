from typing import List
def read_flow_logs(log_file: str) -> str:  
    with open(log_file, "r") as file:
        content = file.read()
    # print(content.split("\n"))
    preprocess_logs(content)
    return content

def preprocess_logs(content: str) -> List[str]:
    lines = content.split("\n")
    processed_lines = [l.strip() for l in lines]
    return processed_lines
    
    

if __name__ == "__main__":
    read_flow_logs("./data/input/flow_logs.txt")