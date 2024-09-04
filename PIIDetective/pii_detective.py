from file_reader import read_text_from_file
from pii_regex import pii_regex,doc_pii_regex 

def pii_detect(file):
    results = []
    
    for label, pattern in {**pii_regex, **doc_pii_regex}.items():
        matches = pattern.findall(read_text_from_file(file))
        if matches:
            for match in matches:
                results.append((label, match))
    
    return results


