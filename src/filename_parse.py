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
        if "-" in time_str and len(time_str.split("-")) == 2:
            # replace the time spliter from ":" to "_" to aviod filename mistake in Windows
            # Should be recover to ":" when applied in Linux.
            self.start = time.strptime(time_str.split("-")[0], "%H_%M_%S")
            self.end = time.strptime(time_str.split("-")[1], "%H_%M_%S")
        else:
            raise ValueError("Invalid Input Time Format")


class Filename(object):
    def __init__(self, filename):
        # First. remove the directory info if exists.
        filename = filename.split("/")[-1]
        if ".log.gz" in filename:
            filename.replace(".log", "")
        filename_list = filename.split(".")

        if len(filename_list) == 2:
            self.protocol = filename_list[0]
            self.time_gap = TimePeriod(filename_list[1])
        else:
            raise ValueError("Invalid Input Filename Format.")

    def is_overlap(self, time_period):
        """
        1. if time_period starts early but ends late (than the start time of self.gap) return True
        2. if time_period starts later bue ends early(than the end time of self.gap) return True
        3. Else, return False
        :param time_period:
        :return:
        """
        if time_period.start >= self.time_gap.start > time_period.end:
            return True
        elif self.time_gap.start >= time_period.start > self.time_gap.end:
            return True
        else:
            return False


class TripleKey(object):
    def __init__(self, str):
        str.strip()
        str_list = str.split(" ")
        if len(str_list) == 4:
            self.sip = ipaddress.ip_address(str_list[1])
            self.dip = ipaddress.ip_address(str_list[2])
            self.dport = str_list[3]
        else:
            raise ValueError("Invalid Input TripleKey Format.")