import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import os

# 定义故障类型
FAULT_TYPES = {
    'meter': [
        '堵塞',
        '泄漏',
        '传感器故障',
        '安装问题',
        '电源问题',
        '流体特性变化',
        '零点漂移',
        '阀门未完全打开',
        '电磁干扰',
        '水流冲击',
        '系统泄漏',
        '水质变化',
        '安装不当',
        '阀门问题'
    ],
    'pipe': [
        '漏水',
        '堵塞',
        '腐蚀',
        '管道破裂',
        '水质问题'
    ],
    'pump': [
        '轴承磨损',
        '叶轮损坏',
        '密封泄漏',
        '电机过热',
        '振动异常',
        '气蚀',
        '效率降低',
        '噪音异常',
        '轴承损坏'
    ]
}

def generate_timestamps(start_time, end_time, interval_minutes=10):
    timestamps = []
    current = start_time
    while current <= end_time:
        timestamps.append(current)
        current += timedelta(minutes=interval_minutes)
    return timestamps

def format_percentage(value):
    """将小数转换为百分比格式"""
    return f"{value * 100:.2f}%"

def generate_history_meter_data(num_devices=30):
    start_time = datetime.strptime("2024-11-06 12:00:33", "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime("2024-11-06 15:55:33", "%Y-%m-%d %H:%M:%S")
    timestamps = generate_timestamps(start_time, end_time)
    
    caliber_types = {
        'small': 25,
        'medium': 50,
        'large': 100
    }
    
    data = []
    for device_id in range(1, num_devices + 1):
        device_name = f"WM_{device_id:03d}"
        caliber_type = np.random.choice(['small', 'medium', 'large'])
        caliber_value = caliber_types[caliber_type]
        
        for ts in timestamps:
            fault_prob = round(np.random.uniform(0, 1), 4)
            row = {
                'device_id': device_name,
                'timestamp': ts.strftime("%Y-%m-%d %H:%M:%S"),
                'flux': round(np.random.uniform(1, 8), 2),
                'pressure': round(np.random.uniform(0.3, 0.8), 2),
                'signal': round(np.random.uniform(-85, -75), 2),
                'voltage': round(np.random.uniform(5.8, 6.2), 2),
                'ph': round(np.random.uniform(6.8, 8.2), 2),
                'turb': round(np.random.uniform(0.5, 4.5), 2),
                'ozone': round(np.random.uniform(0.02, 0.08), 2),
                'caliber': caliber_value,
                'fault_probability': format_percentage(fault_prob),
                'fault_type': np.random.choice(FAULT_TYPES['meter']) if fault_prob > 0.75 else '正常'
            }
            data.append(row)
    
    return pd.DataFrame(data)

def generate_history_pipe_data(num_devices=30):
    start_time = datetime.strptime("2024-11-06 12:00:33", "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime("2024-11-06 15:55:33", "%Y-%m-%d %H:%M:%S")
    timestamps = generate_timestamps(start_time, end_time)
    
    caliber_types = {
        'small': 50,
        'medium': 150,
        'large': 300
    }
    
    data = []
    for device_id in range(1, num_devices + 1):
        device_name = f"PP_{device_id:03d}"
        caliber_type = np.random.choice(['small', 'medium', 'large'])
        caliber_value = caliber_types[caliber_type]
        
        for ts in timestamps:
            fault_prob = round(np.random.uniform(0, 1), 4)
            row = {
                'device_id': device_name,
                'timestamp': ts.strftime("%Y-%m-%d %H:%M:%S"),
                'pipe_stage': np.random.randint(1, 8),
                'pipe_age': round(np.random.uniform(2, 15), 2),
                'pipe_diameter': caliber_value,
                'pipe_length': round(np.random.uniform(2, 8), 2),
                'pipe_pressure': round(np.random.uniform(2, 4), 2),
                'flux': round(np.random.uniform(2, 15), 2),
                'bury_depth': round(np.random.uniform(1.2, 1.8), 2),
                'caliber': caliber_value,
                'fault_probability': format_percentage(fault_prob),
                'fault_type': np.random.choice(FAULT_TYPES['pipe']) if fault_prob > 0.75 else '正常'
            }
            data.append(row)
    
    return pd.DataFrame(data)

def generate_history_pump_data(num_devices=30):
    start_time = datetime.strptime("2024-11-06 12:00:33", "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime("2024-11-06 15:55:33", "%Y-%m-%d %H:%M:%S")
    timestamps = generate_timestamps(start_time, end_time)
    
    caliber_types = {
        'small': 40,
        'medium': 100,
        'large': 200
    }
    
    data = []
    for device_id in range(1, num_devices + 1):
        device_name = f"PM_{device_id:03d}"
        caliber_type = np.random.choice(['small', 'medium', 'large'])
        caliber_value = caliber_types[caliber_type]
        
        for ts in timestamps:
            fault_prob = round(np.random.uniform(0, 1), 4)
            row = {
                'device_id': device_name,
                'timestamp': ts.strftime("%Y-%m-%d %H:%M:%S"),
                'temp': round(np.random.uniform(20, 45), 2),
                'shake': round(np.random.uniform(50, 150), 2),
                'humidity': round(np.random.uniform(30, 70), 2),
                'flux': round(np.random.uniform(5, 15), 2),
                'power': round(np.random.uniform(2, 5), 2),
                'noise': round(np.random.uniform(65, 85), 2),
                'caliber': caliber_value,
                'fault_probability': format_percentage(fault_prob),
                'fault_type': np.random.choice(FAULT_TYPES['pump']) if fault_prob > 0.75 else '正常'
            }
            data.append(row)
    
    return pd.DataFrame(data)

def main():
    base_path = os.path.join(os.path.dirname(__file__), 'data', 'history')
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    
    # 生成数据
    meter_data = generate_history_meter_data()
    pipe_data = generate_history_pipe_data()
    pump_data = generate_history_pump_data()
    
    # 保存CSV文件
    meter_data.to_csv(os.path.join(base_path, 'water_meter_history.csv'), index=False)
    pipe_data.to_csv(os.path.join(base_path, 'water_pipe_history.csv'), index=False)
    pump_data.to_csv(os.path.join(base_path, 'water_pump_history.csv'), index=False)
    
    # 保存JSON文件（格式化输出）
    for name, data in [
        ('water_meter_history.json', meter_data),
        ('water_pipe_history.json', pipe_data),
        ('water_pump_history.json', pump_data)
    ]:
        file_path = os.path.join(base_path, name)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(
                json.loads(data.to_json(orient='records')),
                f,
                indent=2,
                ensure_ascii=False
            )

if __name__ == "__main__":
    main() 