import re
from datetime import datetime, timedelta
from collections import OrderedDict
from time import time

file_path = r"E:\Deepthi\Demo.txt"
time_pattern = re.compile(r"(\d{1,2}:\d{2})")
format_data = "%H:%M"
time_diff = 15

def read_file(file_path):
    with open(file_path) as  _file:
        lines = [each_line.strip() for each_line in _file.readlines()]
    return lines

def different_time_formats(data):
    data_dict = OrderedDict()
    for line in data:
        results = re.findall(time_pattern, line)
        if results:
            req_time = "".join(results)
            if req_time not in data_dict:
                data_dict[req_time] = []
            data_dict[req_time].append(line)
    return data_dict

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def sort_time_based(data_dict):
    print("data_dict", data_dict.keys())
    _dictionary = OrderedDict()
    start_time = datetime.strptime(list(data_dict.keys())[0], format_data)
    end_time = start_time + timedelta(minutes = time_diff)
    for each_time in data_dict:
        current_time = datetime.strptime(each_time, format_data)
        if time_in_range(start_time, end_time, current_time):
            print("yes", current_time)
        else:
            print("no", current_time)
    return _dictionary
        



# data = read_file(file_path)
# time_zones = different_time_formats(data)
# sorted_dict = sort_time_based(time_zones)
# print(sorted_dict.keys())

format_data = "%H:%M"
time_data1 = '03:45'
time_data2 = '04:15'
tstart = datetime.strptime(time_data1, format_data)
tend = datetime.strptime(time_data2, format_data)
interval = timedelta(minutes=15)
periods = []

period_start = tstart
while period_start < tend:
    period_end = min(period_start + interval, tend)
    periods.append((period_start, period_end))
    period_start = period_end
print(periods)

# print(time1.minute)
# print(type(time1.minute))
# print(type(time2-time1))
# print(time2-time1)




# def sort_time_based(data_dict):
#     _dictionary = OrderedDict()
#     start_time = datetime.strptime(list(data_dict.keys())[0], format_data)
#     end_time = start_time + timedelta(minutes = time_diff)
#     print("start_time", start_time)
#     all_data = []
#     for each_time in data_dict:
#         all_data.append(data_dict[each_time])
#         print("each_time", each_time)
#         end_time = datetime.strptime(each_time, format_data)
#         diff_time = end_time - start_time
#         diff_minutes = int(divmod(diff_time.total_seconds(), 60)[0])
#         print("diff_minutes", diff_minutes)
#         if diff_minutes <= time_diff:
#             key_str = "{}-{}".format(start_time, end_time)
#             print("@38", key_str)