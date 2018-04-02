#!/bin/python3
# Script to analysis the RDP traffic in ip_filter file.
# Draw some useful graphs to analysis the results.
# By Zhengping on March 16, 2018.


from src.records import SingleRecord
from src.records import HourlyRecord
from src.records import DailyRecord
import os
from collections import OrderedDict
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data_dict = OrderedDict()
    for filename in os.listdir("../data/ip_filter"):
        # print(filename)
        full_path = "../data/ip_filter/%s" % filename
        daily = DailyRecord(filename)
        cur_hour = None
        with open(full_path) as f:
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
    month_dict = ["2017-08", "2017-09", "2017-10", "2018-02"]
    monthly_count_dict = {month_dict[0]: [],
                          month_dict[1]: [],
                          month_dict[2]: [],
                          month_dict[3]: []}
    total_count_list = []
    for date in data_dict.keys():
        month = "-".join(date.split("-")[:-1])
        # print(month)
        for hour in range(0, 24):
            count = data_dict[date].daily_record["%02d"%hour].get_total_count()
            monthly_count_dict[month].append(count)

    start = 0
    for month in monthly_count_dict.keys():
        plt.plot(range(start, start + len(monthly_count_dict[month])), monthly_count_dict[month])
        start += len(monthly_count_dict[month])

    plt.xlabel("Time (Hour).")
    plt.ylabel("# of sessions per hour.")
    plt.show()