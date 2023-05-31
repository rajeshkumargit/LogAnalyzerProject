#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 13:56:30 2023

@author: rajeshkumar
"""

from src.LogAnalyzer import LogAnalyzer
from src.LogStats import LogStats

if __name__ == '__main__':
    log_file_path = './data/mq.log'

    analyzer = LogAnalyzer(log_file_path)
    analyzer.number_of_warnings()
    analyzer.error_package_names()
    df  = analyzer.parse_requests()

    log_stats = LogStats(df)
    log_stats.transactions_aggregate()
    log_stats.group_by_failure_msg()
    log_stats.generate_trade_flow_chart()
    log_stats.generate_trade_flow_distribution_chart()
    log_stats.generate_quantity_by_symbol_chart()
    log_stats.requests_per_second()
    log_stats.avg_processing_time()