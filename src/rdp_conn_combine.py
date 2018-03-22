#!/usr/bin/python
# Used to select the data from RDP log based on the S_ip, D_ip and D_port.
# print all the output files to output folder.
# By Zhengping, March 20, 2018

from src.filename_parse import TimePeriod, Filename, TripleKey
import os


def file_listing(location, key):
    """
    Find all files in Location that contains "key"
    :param location:
    :param key:
    :return: a list of filename which all contain key.
    """
    selected_file_list = []
    for filename in os.listdir(location):
        if key in filename:
            fname_ojb = Filename(filename)
            selected_file_list.append(fname_ojb)
    return selected_file_list


def time_period_extract(heading_line):
    period = None
    if len(heading_line.split(" ")) == 2:
        line = heading_line.split(" ")[1]
        period = line.strip(":")
    return TimePeriod(period)


def output_filename_generate(source_name, triple_key):
    simp_sour_name = source_name.replace(".log.gz", "")
    return simp_sour_name + "-%s-%s-%s.log" % \
                                       (str(triple_key.sip), str(triple_key.dip), str(triple_key.dport))



if __name__ == '__main__':
    rdp_descriptor_filename = "../data/rdp_conn_comb/2018-02-01"
    source_folder = "../data/rdp_conn_comb/"
    output_folder = "../output/"
    conn_fname_list = file_listing(source_folder, "conn.")
    selected_conn_log = []
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
                """
                time_period = time_period_extract(line)
                for conn_fname in conn_fname_list:
                    if conn_fname.is_overlap(time_period):
                        # This gives the list of conn logs that related to this time period
                        selected_conn_log.append(str(conn_fname))

            elif status == "IN":
                t_key = TripleKey(line)
                for target_conn_log in selected_conn_log:
                    # Generate the Output filename
                    output_filename = output_filename_generate(target_conn_log, t_key)
                    output_file = open(output_filename, "w+")

                    with open(source_folder + target_conn_log) as conn:
                        for conn_line_orig in conn:
                            if "#" in conn_line_orig:
                                continue
                            conn_line = conn_line_orig.strip()
                            conn_line_list = conn_line.split("\t")
                            if (conn_line_list[2] == str(t_key.sip) and
                                        conn_line_list[4] == str(t_key.dip) and
                                        conn_line_list[5] == str(t_key.dport)):
                                output_file.write(conn_line_orig)

            elif status == "END":
                """
                "  destruct parameters used in "ENTER"
                """
                selected_conn_log = []
                print("==== END of Processing %s ====" % rdp_descriptor_filename)


