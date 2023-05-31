#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 12:56:55 2023

@author: rajeshkumar
"""

import re
import pandas as pd

class LogAnalyzer:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path


    def number_of_warnings(self):
        warnings_count = 0
        with open(self.log_file_path, 'r') as log_file:
            for line in log_file:
                if re.search(r'\bWARN\b', line):
                    warnings_count += 1
        print ("\nAnswer to General Comprehension: Question #2:\n")
        print("Total number of log warnings:", warnings_count)
    
    def error_package_names(self):
        pattern = r"\| ERROR \|.*?(\w+\.\w+\.\w+.\w+.\w+\.\w+)"
        with open(self.log_file_path, 'r') as log_file:
            file_str = log_file.read()
            package_names = set(re.findall(pattern, file_str, re.MULTILINE))
        print ("Answer to General Comprehension: Question #3:\n")    
        print(package_names)
    
    def parse_requests(self):
        # Regular expression patterns to extract information
        from_pattern = r"\[FROM\]: \[(.*?)(?=\[RESP\])[\s\S]*"
        resp_pattern = "\[RESP\]: .*?proc:(?P<proc>\d+.\d+).*?httpStatus:(\d+).*?\}"
        
        # Read log file
        with open(self.log_file_path, 'r') as file:
            log_lines = file.readlines()
            
        # Create an empty list to store dictionaries
        data_list = []
        
     # Create an empty DataFrame
        df = pd.DataFrame()
        
        # Process each line in the log file
        for log_statement in log_lines:
            # Check for httpStatus 200
            if 'httpStatus:' in log_statement:
                # Extract [FROM] section
                from_match = re.search(from_pattern, log_statement,re.DOTALL)
                if from_match:
                    from_section = from_match.group(1)
                    from_key_value_matches = re.findall(r"(\w+):([^ ]+)", from_section)
                    from_data = {}
                    for match in from_key_value_matches:
                        key = match[0]
                        value = match[1]
                        from_data[key] = value
        
                # Extract [RESP] section
                resp_match = re.search(resp_pattern, log_statement)
                if resp_match:
                    resp_section = resp_match.group()
                    resp_key_value_matches = re.findall(r"\"(\w+)\":\"([^\"]*)\"|\"(\w+)\":(\d+)", resp_section)
                    resp_data = {}
                    for match in resp_key_value_matches:
                        key = match[0] or match[2]
                        value = match[1] or int(match[3])
                        resp_data[key] = value
                    # Add 'httpStatus' to resp_data dictionary
                    http_status = resp_match.group(2)
                    resp_data['httpStatus'] = http_status

                    # Retrieve 'proc' entry from resp capture group
                    proc_entry = resp_match.group('proc')
                    if proc_entry:
                        resp_data['proc'] = proc_entry
        
                    # Merge [FROM] and [RESP] data
                    merged_data = {**from_data, **resp_data}
        
                    #Append merged data as a new row to the DataFrame
                    data_list.append(merged_data)
                    
        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame.from_records(data_list)
    
        # Convert 'httpStatus' column to numeric type
        df['httpStatus'] = pd.to_numeric(df['httpStatus'])
    
        # Create 'transact_status' column based on 'httpStatus'
        df['transact_status'] = df['httpStatus'].apply(lambda x: 'Success' if x == 200 else 'Failure')
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df[['quantity', 'price', 'proc']] = df[['quantity', 'price', 'proc']].apply(pd.to_numeric, errors='coerce')
        
        return df

        
