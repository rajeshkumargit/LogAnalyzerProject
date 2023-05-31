#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 13:48:02 2023

@author: rajeshkumar
"""

import matplotlib.pyplot as plt

class LogStats:
    def __init__(self, df):
        self.df = df
        
    def transactions_aggregate(self):
        aggregated_df = self.df.groupby(['transact_status', 'type', 'side']).size().reset_index(name='count')
        print("Information Extraction: Question #1:")
        print("\nTransaction Status Aggregate:\n")
        print(aggregated_df)

    
    def group_by_failure_msg(self):        
        self.df[['side', 'type']] = self.df[['side', 'type']].fillna('Unknown')
        failure_df = self.df[self.df['transact_status'] == 'Failure'].groupby(['transact_status', 'type', 'side', 'msg']).size().reset_index(name='count')
        print("\nInformation Extraction: Question #1:")
        print("\nFailure Messages Grouped:\n")
        print(failure_df)
        
    def requests_per_second(self):
        self.df.set_index('timestamp', inplace=True)
        requests_per_sec = self.df.resample('1S').size()
        
        print("Information Extraction: Question #3:")
        print("\nRequests per Second Aggregated Stats:\n")

        plt.plot(requests_per_sec)
        plt.xlabel('Time')
        plt.ylabel('Requests per Second')
        plt.title('Requests per Second Aggregated Stats')
        plt.show()
        
        self.df.reset_index()

    def avg_processing_time(self):
        avg_processing_times = {}
        avg_processing_time = self.df['proc'].astype(float).mean()
        avg_processing_times['Average Processing Time'] = avg_processing_time

        print("Information Extraction: Question #3:")
        print("Processing Time:\n")
        
        plt.plot(self.df['proc'], 'bo', label='Processing Time')
        plt.axhline(avg_processing_time, color='r', linestyle='-', label='Average Processing Time')
        plt.xlabel('Requests')
        plt.ylabel('Processing Time (ms)')
        plt.title('Processing Time vs Average Processing Time')
        plt.legend()

        plt.ylim(0, 300)
        plt.show()

    def generate_trade_flow_chart(self):
        
        print("Information Extraction: Question #1:")
        print("\nTrade Flow Over Time:\n")
        
        plt.plot(self.df['timestamp'], range(len(self.df)))
        plt.xlabel('Timestamp')
        plt.ylabel('Trade Flow')
        plt.title('Trade Flow Over Time')
        plt.xticks(rotation=45)
        plt.show()

    def generate_trade_flow_distribution_chart(self):
        grouped_df = self.df.groupby(['side', 'type']).size().reset_index(name='count')

        print("Information Extraction: Question #1:")
        print("\nTrade Flow Distribution:\n")
        
        plt.bar(grouped_df['side'] + ' - ' + grouped_df['type'], grouped_df['count'])
        plt.xlabel('Trade')
        plt.ylabel('Count')
        plt.title('Trade Flow Distribution')
        plt.xticks(rotation=90)
        plt.show()

    def generate_quantity_by_symbol_chart(self):
        aggregated_df = self.df.groupby('symbol').agg({'quantity': 'sum', 'price': 'mean'}).reset_index()

        print("Information Extraction: Question #1:")
        print("\nTrade Flow: Total Quantity by Symbol:\n")
        
        aggregated_df.plot(x='symbol', y='quantity', kind='bar')
        plt.xlabel('Symbol')
        plt.ylabel('Total Quantity')
        plt.title('Trade Flow: Total Quantity by Symbol')
        plt.show()