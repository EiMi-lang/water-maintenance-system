import pandas as pd
import numpy as np
import json
from datetime import datetime
import os

# 创建数据存储目录
def create_directories():
    base_path = os.path.join(os.path.dirname(__file__), 'data')
    for dir_name in ['logs', 'json']:
        path = os.path.join(base_path, dir_name)
        if not os.path.exists(path):
            os.makedirs(path)
    return base_path

# 生成水表数据
def generate_meter_data(num_devices=30):
    timestamp = "2024-11-06 16:05:33"
    
    # 定义口径类型
    caliber_types = {
        'small': 25,    # 小口径
        'medium': 50,   # 中口径
        'large': 100    # 大口径
    }
    
    data = []
    for device_id in range(1, num_devices + 1):
        device_name = f"WM_{device_id:03d}"
        # 随机选择一种口径
        caliber_type = np.random.choice(['small', 'medium', 'large'])
        caliber_value = caliber_types[caliber_type]
        
        row = {
            'device_id': device_name,
            'timestamp': timestamp,
            'flux': round(np.random.uniform(1, 8), 2),
            'pressure': round(np.random.uniform(0.3, 0.8), 2),
            'signal': round(np.random.uniform(-85, -75), 2),
            'voltage': round(np.random.uniform(5.8, 6.2), 2),
            'ph': round(np.random.uniform(6.8, 8.2), 2),
            'turb': round(np.random.uniform(0.5, 4.5), 2),
            'ozone': round(np.random.uniform(0.02, 0.08), 2),
            'caliber': caliber_value
        }
        data.append(row)
    
    return pd.DataFrame(data)

# 生成水管数据
def generate_pipe_data(num_devices=30):
    timestamp = "2024-11-06 16:05:33"
    
    # 定义口径类型
    caliber_types = {
        'small': 50,     # 小口径
        'medium': 150,   # 中口径
        'large': 300     # 大口径
    }
    
    data = []
    for device_id in range(1, num_devices + 1):
        device_name = f"PP_{device_id:03d}"
        caliber_type = np.random.choice(['small', 'medium', 'large'])
        caliber_value = caliber_types[caliber_type]
        
        row = {
            'device_id': device_name,
            'timestamp': timestamp,
            'pipe_stage': np.random.randint(1, 8),
            'pipe_age': round(np.random.uniform(2, 15), 2),
            'pipe_diameter': caliber_value,
            'pipe_length': round(np.random.uniform(2, 8), 2),
            'pipe_pressure': round(np.random.uniform(2, 4), 2),
            'flux': round(np.random.uniform(2, 15), 2),
            'bury_depth': round(np.random.uniform(1.2, 1.8), 2),
            'caliber': caliber_value
        }
        data.append(row)
    
    return pd.DataFrame(data)

# 生成水泵数据
def generate_pump_data(num_devices=30):
    timestamp = "2024-11-06 16:05:33"
    
    # 定义口径类型
    caliber_types = {
        'small': 40,     # 小口径
        'medium': 100,   # 中口径
        'large': 200     # 大口径
    }
    
    data = []
    for device_id in range(1, num_devices + 1):
        device_name = f"PM_{device_id:03d}"
        caliber_type = np.random.choice(['small', 'medium', 'large'])
        caliber_value = caliber_types[caliber_type]
        
        row = {
            'device_id': device_name,
            'timestamp': timestamp,
            'temp': round(np.random.uniform(20, 45), 2),
            'shake': round(np.random.uniform(50, 150), 2),
            'humidity': round(np.random.uniform(30, 70), 2),
            'flux': round(np.random.uniform(5, 15), 2),
            'power': round(np.random.uniform(2, 5), 2),
            'noise': round(np.random.uniform(65, 85), 2),
            'caliber': caliber_value
        }
        data.append(row)
    
    return pd.DataFrame(data)

def main():
    base_path = create_directories()
    
    # 生成数据
    meter_data = generate_meter_data()
    pipe_data = generate_pipe_data()
    pump_data = generate_pump_data()
    
    # 保存CSV文件
    csv_path = os.path.join(base_path, 'logs')
    meter_data.to_csv(os.path.join(csv_path, 'water_meter_test.csv'), index=False)
    pipe_data.to_csv(os.path.join(csv_path, 'water_pipe_test.csv'), index=False)
    pump_data.to_csv(os.path.join(csv_path, 'water_pump_test.csv'), index=False)
    
    # 保存JSON文件（格式化输出）
    json_path = os.path.join(base_path, 'logs')
    for name, data in [
        ('water_meter_test.json', meter_data),
        ('water_pipe_test.json', pipe_data),
        ('water_pump_test.json', pump_data)
    ]:
        file_path = os.path.join(json_path, name)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(
                json.loads(data.to_json(orient='records')),
                f,
                indent=2,
                ensure_ascii=False
            )

if __name__ == "__main__":
    main()