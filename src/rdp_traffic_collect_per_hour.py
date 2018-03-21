import os
from collections import OrderedDict
from matplotlib import pyplot as plt
import numpy as np


class CountRecord(object):
    def __init__(self, time_period, count):
        self.time_period = time_period
        self.time_start = time_period.split("-")[0]
        self.count = int(count)

    def __str__(self):
        return "In time period %s, # of recorded request is %d\n" % \
               (self.time_period, self.count)


class RecordBin(object):

    def __init__(self):
        self.daily_record = {}
        for time_hour in range(0, 24):
            time_stamp = "%02d" % time_hour
            self.daily_record[time_stamp] = 0
            # print(time_stamp)

    def __str__(self):
        out_str = ""
        for time_hour in self.daily_record.keys():
            out_str += "%s:00:00-%02d:00:00\t%d\n" % \
                   (time_hour, int(time_hour)+1, self.daily_record[time_hour])
        return out_str

    def insert(self, count_record):
        time_hour = count_record.time_start.split(":")[0]
        self.daily_record[time_hour] += count_record.count


class RdpAnalysis(object):
    def __init__(self, record):
        self.record = record

    def draw_plot(self):
        result_bin = []
        xticks_index = []
        xticks = []
        for date in self.record.keys():
            daily_record = self.record[date].daily_record.values()
            print(daily_record)
            for value in daily_record:
                result_bin.append(value)
        print(result_bin)
        plt.plot(np.arange(0, len(result_bin)), result_bin)
        plt.ylim(0, 7000)
        for cut_line_index in range(0, len(result_bin)):
            if cut_line_index%24 == 0:
                xticks_index.append(cut_line_index)
                plt.plot([cut_line_index, cut_line_index], [0, 7000], linewidth=1, color="lightskyblue", linestyle="--")
        xticks = self.record.keys()

        plt.xticks(xticks_index, xticks)
        plt.xlabel("Date.")
        plt.ylabel("RDP Records Per Hour.")
        plt.show()



if __name__ == '__main__':
    log_folder = './data/conn_per_hour/'
    output_folder = './data/updated_conn_per_hour/'

    total_record = OrderedDict()
    for filename in os.listdir(log_folder):
        print(filename)
        if("2017-09-0" in filename):
            with open(log_folder + filename, 'r') as f:
                rbin = RecordBin()
                for line in f:
                    countRecord = CountRecord(line.split("\t")[0], line.split("\t")[1])
                    rbin.insert(countRecord)
                # print(rbin)
                total_record[filename] = rbin
                # with open(output_folder + filename + "_updated", 'w') as out_f:
                    # out_f.write(str(rbin))

    rdp = RdpAnalysis(total_record)
    rdp.draw_plot()
