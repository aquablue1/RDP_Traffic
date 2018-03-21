#/bin/python3
# Script to filter all Private Ip addresses from the IP description list.
# Because we do not need the private IP address in the analysis
# There are are two reasons to explain why we do not need:
# 1. most private addresses are innocent
# 2. the record of private address in our monitor is not accurate

import ipaddress
import os
import time
from src.ip_lookup import ResearchIP
from src.records import SingleRecord, HourlyRecord, DailyRecord

if __name__ == '__main__':

    data_dict = {}

    log_folder = '../data/ip_filter/'
    output_folder = './data/results_ip_filter/'
    for filename in os.listdir(log_folder):
        print(filename)
        with open('../data/ip_filter/%s' % filename) as f:
            # Generate the descriptor for a daily data.
            daily = DailyRecord(filename)
            cur_hour = None
            for line in f:
                if line.startswith("##"):
                    # start a hourly record
                    line = line.strip(": \n")
                    time_period = line.split(" ")[1]
                    cur_hour = time_period[0:2]
                elif len(line.strip().split(" ")) == 6:
                    single = SingleRecord(line.strip().split(" "))
                    daily.daily_record[cur_hour].insert_single_record(single)

            data_dict[filename] = daily
    print(data_dict)

    # GET the suspicious IP addresses in each hour
    ip_to_lookup = []
    for daily in data_dict.values():
        for hour in daily.daily_record.keys():
            ip_to_lookup += daily.daily_record[hour].get_suspicious_ip_list()
    ip_to_lookup_uniq = set(ip_to_lookup)
    print(ip_to_lookup_uniq)
    print(len(ip_to_lookup_uniq))

    # match them in both BASIC and ABUSE IP database.

    # CONNECT

    for ip in ip_to_lookup_uniq:
        research_ip = ResearchIP(ip)
        print("======= Info for IP: %s =========\n" % ip)
        ResearchIP.print_to_log("\n======= Info for IP: %s =========" % ip)
        ResearchIP.print_to_error("\n********** Errors for IP: %s ************" % ip)
        research_ip.find_basic()
        research_ip.find_abuse()
        time.sleep(1)

    # END CONNECT



