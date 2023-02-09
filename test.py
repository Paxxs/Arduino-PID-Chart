import matplotlib.pyplot as plt
import serial
import csv
from datetime import datetime as d

# cspell:words ioff baudrate


def init_plot(
    title: str = "pid graph", x_label: str = "x(Time)", y_label: str = "value"
):
    fig = plt.figure()
    ax = fig.add_subplot()

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    ax.grid(True)
    return fig, ax


def draw_graph(
    time: int = 0,
    output: float = 0.0,
    temp: float = 0.0,
    setpoint: float = 25.00,
    max_output=255,  # 控制输出最大值
):
    fig, ax = init_plot()

    # 初始数据
    pid_time_array = [  # 时间
        time,
    ]
    pid_output_array = [  # 输出
        output,
    ]
    pid_input_array = [  # 温度
        temp,
    ]

    temp_t = ax.plot(pid_time_array, pid_input_array, "-r", label="Temp")[0]
    output_t = ax.plot(
        pid_time_array,
        [i * (max_output / 255) for i in pid_output_array],
        "-b",
        label="pid output",
    )[0]
    setpoint_t = ax.plot(
        [pid_time_array[0], pid_time_array[-1]],
        [setpoint, setpoint],
        "-.y",
        label="setpoint",
    )[0]
    plt.legend(loc="best")
    plt.ion()

    # 控制图的最大最小
    x_min, x_max = 0, 10
    y_min, y_max = 0, (setpoint + 3) if setpoint > 0 else 10

    def judge_xy_range(value, is_x: bool = True):
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

    def update_graph(time: int, output: float, temp: float, setpoint: float = setpoint):
        """更新绘图

        Args:
            time (int): 时间
            output (float): pid 输出
            temp (float): 温度
            setpoint (float, optional): 设定值. Defaults to setpoint.

        Returns:
            Axes: plt
        """
        nonlocal pid_time_array, pid_output_array, pid_input_array
        nonlocal temp_t, output_t, setpoint_t, max_output
        nonlocal x_max, x_max, y_max, y_min

        # 更新数组
        pid_time_array.append(judge_xy_range(time))
        pid_output_array.append(judge_xy_range(output, False))
        pid_input_array.append(judge_xy_range(temp, False))

        # 更新图
        temp_t.set_data(pid_time_array, pid_input_array)
        output_t.set_data(
            pid_time_array, [i * (max_output / 255) for i in pid_output_array]
        )
        setpoint_t.set_data(
            [pid_time_array[0], pid_time_array[-1]], [setpoint, setpoint]
        )

        # 更新图范围
        ax.set_xlim([x_min, x_max + 5])
        ax.set_ylim([y_min, y_max + 5])
        return ax

    return update_graph, ax


def read_from_com(ser: serial.Serial, sep: str = "-"):
    """从 Serial 读取数据并按 sep 分割

    Args:
        ser (serial.Serial): Serial
        sep (str): 分隔符

    Returns:
        List[str]: 分割后的数组
    """
    line_str = ser.readline().decode().rstrip()
    return line_str.split(sep)


def init_csv_writer(
    data, name: str = f'./data/data-{d.now().strftime("%Y%m%d-%H_%M_%S")}.csv'
):
    """初始化 csv writer，并返回写入回调函数

    Args:
        data (任何可迭代对象): 写入的数据
        name (str, optional): csv 名称. Defaults to f'./data-{d.now().strftime("%Y%m%d-%H_%M_%S")}.csv'.
    Returns:
        function: write
    """

    def write(data):
        with open(name, "a") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(data)

    write(data)
    return write


# 配置项：
serial_com = "COM5"
serial_baudrate = 9600
setpoint = 28.0

with serial.Serial(serial_com, serial_baudrate) as ser:
    """数据格式
    index   value
    0       时间
    1       温度
    2       输出
    3       加热模式
    """
    lines = read_from_com(ser)
    graph, _ = draw_graph(int(lines[0]), float(lines[2]), float(lines[1]), setpoint)
    plt.show()

    # 存储数据
    header = ["time", "temperature", "output", "heatingMode"]
    write = init_csv_writer(header)
    while True:
        plt.pause(1.3)
        lines = read_from_com(ser)
        print(lines)
        time: int = int(lines[0])
        if lines[0] == "p":
            plt.ioff()
        else:
            plt.ion()
            write(lines)  # 写入
            graph(time, float(lines[2]), float(lines[1]))
