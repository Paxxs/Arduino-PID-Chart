# Arduino PID 温控器测试用绘图工具

给我的 Arduino PID 温控器测试实时绘制图表和数据记录。

## 特性

- 绘制图表
- 数据保存
- 参数输入

## 使用

> 按需修改代码中的配置项

```python
python -m venv venv

# end venv

pip -r requirements.txt

python main.py
```

## 接受的数据格式

| index | value    |
| ----- | -------- |
| 0     | 时间     |
| 1     | 温度     |
| 2     | 输出     |
| 3     | 加热模式 |
