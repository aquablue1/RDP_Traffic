#/bin/python
# definition of several record related records:
# 1. SingleRecord: the record object of a single line of record in rdp description file
#       sample single line record input:
#                   1 212.92.124.161 136.159.101.161 6666 hello HYBRID
# 2. HourlyRecord: the record object of one hour record in rdp description file

import ipaddress


class SingleRecord(object):
    def __init__(self, line_record_list):
        if len(line_record_list) == 6:          # the length of line_record_list has to be 6
            # Assign the init counting for this record.
            # this value could be changed in Hourly Record.
            self.count = int(line_record_list[0])

            # Assign both source and dest IP as idaddress type.
            self.ip_source = ipaddress.ip_address(line_record_list[1])

            self.ip_dest = ipaddress.ip_address(line_record_list[2])

            # Assign both port_dst and username as list since we define the single record as
            # unique Source and Destination IP address. Even if the port of username is different,
            # We still think it is possible to belongs to one single record.
            # This design will help us find suspicious Source IP addresses in HourlyRecord.
            self.port_dest_list = [line_record_list[3]]
            self.username_list = [line_record_list[4]]

            self.encryption_method = line_record_list[5]
        else:
            raise ValueError("Length of Input Record is Incorrect.")

    def is_meaningful(self):
        """
        check if this line is meaningful
        IS meaningful if both IPs are not private IP
        :return: Boolean
        """
        if self.ip_source.is_private or self.ip_dest.is_private:
            return False
        else:
            return True

    def get_ip_source(self):
        return self.ip_source

    def get_ip_dest(self):
        return self.ip_dest

    def get_count(self):
        return int(self.count)

    def is_suspicious(self):
        if self.count > 10:
            return True
        else:
            return False


class HourlyRecord(object):
    def __init__(self, time_hour, single_record_list=None):
        if single_record_list is None:
            single_record_list = []
        self.time_hour = time_hour
        # get the starting hour e.g. 02 marks the 2 a.m to 3 a.m period.
        # this is used as an INDEX in DailyRecord.

        self.record_list = []
        # list of the record within the given date and time-period
        # This variable (list) can only be verified by using self.insert_single_record method.

        self.private_count = 0
        for record in single_record_list:
            if record.is_meaningful():
                self.record_list.append(record)

    def get_suspicious_ip_list(self):
        """
        Return all suspicious IP records in this Hourly Record, as list.
        :return:
        """
        suspicious_list = []
        for record in self.record_list:
            if record.is_suspicious():
                suspicious_list.append(record.get_ip_source())
        return suspicious_list

    def get_victim_ip_list(self):
        """
        Return all victim IP records in this Hourly Record, as list.
        :return:
        """
        victim_list = []
        for record in self.record_list:
            if record.is_suspicious():
                victim_list.append(record.get_ip_dest())
        return victim_list

    def get_victim_ip_dict(self):
        """
        Return all victim IP records in this Hourly Record, as dict with value as the # been attacked.
        :return:
        """
        victim_dict = {}
        for record in self.record_list:
            if record.is_suspicious():
                victim_dict[str(record.get_ip_dest())] = record.get_count()
        # print("victim_dict %s" % victim_dict)
        return victim_dict


    def insert_single_record(self, single_record):
        """
        Insert a new Single Record into this hourly list.
        :param single_record:
        :return:
        """
        is_found = False
        if single_record.is_meaningful():
            for record in self.record_list:
                if record.ip_source == single_record.ip_source and record.ip_dest == single_record.ip_dest:
                    is_found = True
                    record.count += single_record.count
                    for username in single_record.username_list:
                        if username not in record.username_list:
                            record.username_list.append(username)
                    for port in single_record.port_dest_list:
                        if port not in record.port_dest_list:
                            record.port_dest_list.append(port)
                    return
            if not is_found:
                self.record_list.append(single_record)
        else:
            # print("input record contains private IP address.")
            return

    def get_total_count(self):
        """
        Return the number counting of records in this Hourly Record.
        Basically add the count in each Single Record.
        :return:
        """
        total_count = 0
        for record in self.record_list:
            total_count += record.count
        return total_count


class DailyRecord(object):
    def __init__(self, date):
        self.date = date
        self.daily_record = {}
        for time_hour in range(0, 24):
            time_stamp = "%02d" % time_hour
            self.daily_record[time_stamp] = HourlyRecord(time_stamp)

    def insert_hourly_record(self, hour_record):
        time_hour = hour_record.time_hour
        self.daily_record[time_hour] = hour_record


if __name__ == '__main__':
    print(" ============== Test Here ===============")
    # s_record = SingleRecord("   1 10.92.124.161 136.159.101.161 6666 hello HYBRID\n")
    # print(s_record.is_meaningful())



