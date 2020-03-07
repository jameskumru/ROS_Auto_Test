import re


class Odometry:
    def __init__(self, raw_input):
        self.x_pos = float(re.search(r": (\d+\.\d+)", raw_input[2]).group(1))
        self.y_pos = float(re.search(r": (\d+\.\d+)", raw_input[3]).group(1))
        self.z_pos = float(re.search(r": (\d+\.\d+)", raw_input[4]).group(1))
        self.x_ori = float(re.search(r": (\d+\.\d+)", raw_input[6]).group(1))
        self.y_ori = float(re.search(r": (\d+\.\d+)", raw_input[7]).group(1))
        self.z_ori = float(re.search(r": (\d+\.\d+)", raw_input[8]).group(1))
        self.w_ori = float(re.search(r": (\d+\.\d+)", raw_input[9]).group(1))
