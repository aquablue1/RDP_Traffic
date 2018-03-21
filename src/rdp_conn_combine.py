#!/usr/bin/python
# Used to select the data from RDP log based on the S_ip, D_ip and D_port.
# print all the output files to output folder.
# By Zhengping, March 20, 2018

from src.filename_parse import TimePeriod, Filename, TripleKey

if __name__ == '__main__':
    rdp_descriptor_filename = "../data/rdp_conn_comb/2018-02-01"
    source_file = "../data/rdp_conn_comb/"
    target_conn_log = None
    with open(rdp_descriptor_filename) as f:
        for line in f:
            line = line.strip()
            if "## " in line:
                status = "ENTER"
            elif line == "##":
                status = "END"
            else:
                status = "IN"

            if status == "ENTER":
                """
                " Get Ready the Target conn filename.
                " And the output filename
                """
                line = line.split(" ")[1]
                period = line.strip(":")
                time_period = TimePeriod(period)
                print(line)
                target_conn_log = "conn.00_00_00-00_00_20.log"
            elif status == "IN":
                t_key = TripleKey(line)
                with open(source_file + target_conn_log) as conn:
                    for conn_line_orig in conn:
                        if "#" in conn_line_orig:
                            continue
                        conn_line = conn_line_orig.strip()
                        conn_line_list = conn_line.split("\t")
                        if (conn_line_list[2] == str(t_key.sip) and
                                    conn_line_list[4] == str(t_key.dip) and
                                    conn_line_list[5] == str(t_key.dport)):
                            print(conn_line_orig)


