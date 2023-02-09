import numpy as np
import matplotlib.pyplot as plt
import time


def init_plot(title="pid graph", x_label='x(Time)', y_label='value'):
    fig = plt.figure()
    ax = fig.add_subplot()

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    ax.grid(True)
    return fig, ax


def draw_graph(time=0, output=0.0, temp=0.0, setpoint=25, max_output=255  # 控制输出最大值
               ):
    fig, ax = init_plot()

    # 初始数据
    pid_time_array = [time,]  # 时间
    pid_output_array = [output,]  # 输出
    pid_input_array = [temp,]  # 温度

    temp_t = ax.plot(pid_time_array, pid_input_array, '-r', label="Temp")[0]
    output_t = ax.plot(pid_time_array, [i * (max_output/255)
                                        for i in pid_output_array], '-b', label="pid output")[0]
    setpoint_t = ax.plot([pid_time_array[0], pid_time_array[-1]],
                         [setpoint, setpoint], '-.y', label="setpoint")[0]
    plt.legend(loc="best")
    plt.ion()

    # 控制图的最大最小
    x_min, x_max = 0, 10
    y_min, y_max = 0, 10

    def judge_xy_range(value, is_x=True):
        """更新 x y 轴上的最大最小范围

        Args:
            value (int/float): 轴上的值
            is_x (bool, optional): 是否为 x 轴. Defaults to True.

        Returns:
            (int/float): 传入的 value
        """
        nonlocal x_min, y_min, x_max, y_max
        if is_x:
            x_min = min(x_min, value)
            x_max = max(x_max, value)
        else:
            y_min = min(y_min, value)
            y_max = max(y_max, value)
        return value

    def update_graph(time, output, temp, setpoint=setpoint):
        nonlocal pid_time_array, pid_output_array, pid_input_array
        nonlocal temp_t, output_t, setpoint_t, max_output
        nonlocal x_max, x_max, y_max, y_min

        # 更新数组
        pid_time_array.append(judge_xy_range(time))
        pid_output_array.append(judge_xy_range(output, False))
        pid_input_array.append(judge_xy_range(temp, False))

        # 更新图
        temp_t.set_data(pid_time_array, pid_input_array)
        output_t.set_data(pid_time_array, [i * (max_output/255)
                                           for i in pid_output_array])
        setpoint_t.set_data([pid_time_array[0], pid_time_array[-1]],
                            [setpoint, setpoint])

        # 更新图范围
        ax.set_xlim([x_min, x_max+5])
        ax.set_ylim([y_min, y_max+5])

        # plt.pause(0.5)
        return update_graph
    return update_graph


graph = draw_graph()
for i in range(1, 30):
    graph = graph(i, i*2, i*2+5+i)




plt.ioff()
plt.show()
