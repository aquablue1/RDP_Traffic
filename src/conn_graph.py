import matplotlib.pyplot as plt
import time

time_list = []
with open('../data/conn/data_slice2.txt', 'r') as f:
    for line in f:
        line = line.strip()
        line_list = line.split(" ")
        print(line_list)
        d_time = time.gmtime(int(float(line_list[0])) - 6*3600)
        print(d_time)
        time_list.append(line_list)

time_start = float(time_list[0][0])
for time in time_list:
    start_point = [float(time[0]) - time_start, float(time[0]) - time_start]
    end_point = [ -int(time[1]), int(time[2])]
    plt.plot(start_point, end_point, color='blue')

plt.ylabel("Byte in(-) and out(+) (Bytes).")
plt.xlabel("Time Series (second).")
plt.show()


