import re
from datetime import datetime, timedelta
from collections import OrderedDict
import os

file_path = r"E:\Deepthi\Demo.txt"
output_dir = os.path.dirname(file_path)
time_pattern = re.compile(r"(\d{2}:\d{2}:\d{2})")
format_data = "%H:%M:%S"
time_diff = 15
required_strings_pattern = re.compile(r"lstat|stat|open|close")
bytes_pattern = r"bytes read (\d+)"

def read_file(file_path):
    with open(file_path) as  _file:
        lines = [each_line.strip() for each_line in _file.readlines() if any(re.findall(required_strings_pattern, each_line.strip()))]
    return lines

def write_file(file_path, data):
    with open(file_path, "w") as file_:
        file_.write(data)


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

def get_total_bytes(list_data):
    total = 0
    for i in list_data:
        m = re.search(bytes_pattern, i, re.IGNORECASE)
        if m:
            total += int(m.group(1))
    return total

def get_time_range(all_times):
    tstart = all_times[0].replace(all_times[0].split(":")[-1], "00")
    tend = all_times[-1].replace(all_times[-1].split(":")[-1], "00")
    tstart_obj = datetime.strptime(tstart, format_data)
    tend_obj = datetime.strptime(tend, format_data)+timedelta(minutes=1)
    interval = timedelta(minutes=time_diff)
    periods = []
    period_start = tstart_obj
    while period_start < tend_obj:
        period_end = min(period_start + interval, tend_obj)
        periods.append((period_start, period_end))
        period_start = period_end
    return periods

def generate_sorted_files(file_path):
    data = read_file(file_path)
    time_zones = different_time_formats(data)
    all_times = list(time_zones.keys())
    time_ranges = get_time_range(all_times)
    sorted_data = OrderedDict()
    for each_time_range in time_ranges:
        start_time = each_time_range[0]
        end_time = each_time_range[1]
        for each_time in time_zones:
            current_time = datetime.strptime(each_time, format_data) 
            if time_in_range(start_time, end_time, current_time):
                key = "{}:{}:{}-{}:{}:{}".format(start_time.hour,start_time.minute,start_time.second , end_time.hour, end_time.minute, end_time.second)
                if key not in sorted_data:
                    sorted_data[key] = []
                sorted_data[key].append(time_zones[each_time])
    generate_files(sorted_data)

def generate_files(data):
    sorted_data = {i:[j for t in data[i] for j in t] for i in data}
    for each_data in sorted_data:
        list_data = sorted_data[each_data]
        VolumeUploaded = get_total_bytes(list_data)
        num_of_files = len(list_data)/4
        TimeTaken = time_diff
        data_to_text = str(each_data)+","+str(VolumeUploaded)+","+str(num_of_files)+","+str(TimeTaken)
        file_name = each_data.replace("-", "_").replace(":", "-")+".txt"
        output_file_path = os.path.join(output_dir, file_name)
        write_file(output_file_path, data_to_text)


generate_sorted_files(file_path)