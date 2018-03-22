#!/usr/bin/python
# Filename Parse class
# Used to parse a filename from a string to several functional parts.
# Accept a string type as the name
# build the object with each function as defined in the filename (string)
# By Zhengping, March 20, 2018.
import time
import ipaddress

class TimePeriod(object):
    def __init__(self, time_str):
        """
        :param time_str: Input format: 21:00:00-22:00:03
        """
        # In stage, ignore the date of the time.
        self.time_str = time_str
        if "-" in time_str and len(time_str.split("-")) == 2:
            # replace the time spliter from ":" to "_" to aviod filename mistake in Windows
            # Should be recover to ":" when applied in Linux.
            self.start = time.strptime(time_str.split("-")[0], "%H:%M:%S")
            self.end = time.strptime(time_str.split("-")[1], "%H:%M:%S")
        else:
            raise ValueError("Invalid Input Time Format")

    def __str__(self):
        return self.time_str

    def is_overlap(self, time_period):
        """
        1. if time_period starts early but ends late (than the start time of self.gap) return True
        2. if time_period starts later bue ends early(than the end time of self.gap) return True
        3. Else, return False
        :param time_period:
        :return:
        """
        if time_period.end > self.start >= time_period.start :
            return True
        elif self.end > time_period.start >= self.start :
            return True
        else:
            return False



class Filename(object):
    def __init__(self, filename):
        # First. remove the directory info if exists.
        filename = filename.split("/")[-1]
        self.filename = filename
        if ".log.gz" in filename:
            filename = filename.replace(".log.gz", "")
        filename_list = filename.split(".")

        if len(filename_list) == 2:
            self.protocol = filename_list[0]
            self.time_gap = TimePeriod(filename_list[1])
        else:
            raise ValueError("Invalid Input Filename Format.")

    def __str__(self):
        return self.filename


class TripleKey(object):
    def __init__(self, str):
        str.strip()
        str_list = str.split(" ")
        if len(str_list) == 4:
            self.sip = ipaddress.ip_address(str(str_list[1]))
            self.dip = ipaddress.ip_address(str(str_list[2]))
            self.dport = str_list[3]
        else:
            raise ValueError("Invalid Input TripleKey Format.")


if __name__ == '__main__':
    tp1 = TimePeriod("23:00:01-00:00:12")
    tp2 = TimePeriod("00:00:01-00:00:11")

    print(tp1.is_overlap(tp2))

    print(tp1.start >= tp2.start)