def calculate_traffic_flow(sensor_data):
    """
    根据传感器数据计算车流量
    :param sensor_data: 传感器输入的车辆计数数据
    :return: 建议的红绿灯类型（single/double/triple）
    """
    flow = sensor_data.get('flow', 0)
    
    if flow < 10:
        return 'left-turn'
    elif 10 <= flow < 30:
        return 'right-turn'
    else:
        return 'straight'