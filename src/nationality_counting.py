#!/usr/bin/python
# Extract nationality info from result/ip_report.log
# By zhengping on March 26, 2018

from collections import Counter
import matplotlib.pyplot as plt

if __name__ == '__main__':
    with open("../results/ip_report_Feb.log") as f:
        flag = False
        nationality_list = []
        for line in f:
            if "===" in line and "136.159" not in line:
                flag = True
                continue
            if flag:
                nationality_list.append(line.split("\t")[1])
                flag = False
    print(len(nationality_list))
    print(len(set(nationality_list)))
    print(Counter(nationality_list).most_common())
    nationality_list.sort()
    nationality_count_list = [y for (x, y) in Counter(nationality_list).most_common()]
    count_all = [86, 47, 44, 41, 11, 56]
    labels_all = ['Netherlands', 'US', 'German', 'Russia', 'Canada', 'Others']
    explode_all = (0.05, 0, 0, 0, 0, 0)
    # plt.pie(count_all, labels = labels_all, autopct='%1.1f%%', radius=1.1, shadow=True, explode=explode_all)
    # plt.show()
    count_feb = [33, 26, 24, 8, 5, 26]
    labels_feb = ['Netherland', 'Russia', 'Germany', 'US', 'France', 'Others']
    explode_feb = (0.05, 0, 0, 0, 0, 0)
    # plt.pie(count_feb, labels=labels_feb, autopct='%1.1f%%', radius=1.1, shadow=True, explode=explode_feb)
    # plt.show()

    count_exfeb = [57, 40, 22, 18, 9, 28]
    labels_exfeb = ['Netherland', 'US', 'Germany', 'Russia', 'Canada', 'Others']
    explode_exfeb = (0.05, 0, 0, 0, 0, 0)
    plt.pie(count_exfeb, labels=labels_exfeb, autopct='%1.1f%%', radius=1.1, shadow=True, explode=explode_exfeb)
    plt.show()