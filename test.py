import numpy as np
import matplotlib.pyplot as plt

"""假动态
"""
fig = plt.figure()
ax = fig.add_subplot()

ax.set_xlabel('x(Time)')
ax.set_ylabel('value')
ax.set_title("pid graph")

ax.grid(True)

# plt.xlabel('x (Time)')
# plt.ylabel('value')
# plt.grid(True)

# 初始数据
# pid_time_array = [1,2,3,4,5]
# pid_output_array = [21.00,30.00,50.00,100.00,255.00]
# pid_input_array = [5.00,5.1,7.2,8.00,9.00]
pid_time_array = [0,]  # 时间
pid_output_array = [0.0,]  # 输出
pid_input_array = [0.00,]  # 温度

max_output = 255  # 控制输出最大值
setpoint = 15  # 设置点

temp_t = ax.plot(pid_time_array, pid_input_array, '-r', label="Temp")[0]
output_t = ax.plot(pid_time_array, [i * (max_output/255)
                                    for i in pid_output_array], '-b', label="pid output")[0]
setpoint_t = ax.plot([pid_time_array[0], pid_time_array[-1]],
                     [setpoint, setpoint], '-.y', label="setpoint")[0]
plt.legend(loc="best")
plt.ion()

# 控制图的最大最小
x_min = 0
y_min = 0
x_max = 10
y_max = 10

def judge_xy_range(value, isX=True):
    global x_min, y_min, x_max, y_max
    if isX:
        if x_min > value:
            x_min = value
        elif x_max < value:
            x_max = value
    else:
        if y_min > value:
            y_min = value
        elif y_max < value:
            y_max = value
    return value


for i in range(30):
    pid_time_array.append(judge_xy_range(pid_time_array[-1]+1))
    pid_output_array.append(judge_xy_range(i*2, False))
    pid_input_array.append(judge_xy_range(i*4-3*1+5, False))

    temp_t.set_data(pid_time_array, pid_input_array)
    output_t.set_data(pid_time_array, [i * (max_output/255)
                                       for i in pid_output_array])
    setpoint_t.set_data([pid_time_array[0], pid_time_array[-1]],
                        [setpoint, setpoint])
    ax.set_xlim([x_min, x_max+5])
    ax.set_ylim([y_min, y_max+5])

    plt.pause(0.5)

plt.ioff()
plt.show()
