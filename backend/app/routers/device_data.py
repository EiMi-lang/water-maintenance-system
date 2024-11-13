from fastapi import APIRouter, HTTPException
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime
from pydantic import BaseModel
import csv
router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/device/{device_type}/{device_id}/flux")
async def get_device_flux_data(device_type: str, device_id: str):
    try:
        # 构建文件路径
        file_name = f"water_{device_type}_history.csv"
        file_path = Path(__file__).parent.parent.parent / "scripts" / "data" / "history" / file_name
        
        logger.info(f"Reading data from {file_path}")
        
        # 检查文件是否存在
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"找不到{device_type}的数据文件")
            
        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        # 过滤指定设备的数据
        device_data = df[df['device_id'] == device_id]
        
        if device_data.empty:
            raise HTTPException(status_code=404, detail=f"找不到设备 {device_id} 的数据")
            
        # 只保留 timestamp 和 flux 字段
        result_data = device_data[['timestamp', 'flux']].copy()
        
        # 转换时间格式和处理 flux 数值
        results = []
        for _, row in result_data.iterrows():
            # 转换时间格式
            timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d %H:%M:%S')
            # 将 flux 转为整数
            flux = int(round(row['flux']))
            
            results.append({
                "name": timestamp,
                "value": [timestamp, flux]
            })
            
        return {
            "results": results
        }
        
    except Exception as e:
        logger.error(f"获取设备数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/device/{device_type}/{device_id}/details")
async def get_device_details(device_type: str, device_id: str):
    try:
        # 定义不同设备类型需要的字段
        type_fields = {
            'meter': ['pressure', 'signal', 'voltage', 'timestamp'],
            'pipe': ['pipe_pressure', 'timestamp'],
            'pump': ['temp', 'shake', 'humidity', 'power', 'noise', 'timestamp']
        }
        
        # 检查设备类型是否有效
        if device_type not in type_fields:
            raise HTTPException(status_code=400, detail=f"不支持的设备类型: {device_type}")
            
        # 构建文件路径
        file_name = f"water_{device_type}_history.csv"
        file_path = Path(__file__).parent.parent.parent / "scripts" / "data" / "history" / file_name
        
        logger.info(f"Reading data from {file_path}")
        
        # 检查文件是否存在
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"找不到{device_type}的数据文件")
            
        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        # 过滤指定设备的数据
        device_data = df[df['device_id'] == device_id]
        
        if device_data.empty:
            raise HTTPException(status_code=404, detail=f"找不到设备 {device_id} 的数据")
            
        # 获取需要的字段
        fields = type_fields[device_type]
        result_data = device_data[fields].copy()
        
        # 首先按时间戳排序
        result_data['timestamp'] = pd.to_datetime(result_data['timestamp'])
        result_data = result_data.sort_values('timestamp')
        
        # 处理数据
        result = {}
        for field in fields:
            if field == 'timestamp':
                # 处理时间格式
                result[field] = [
                    dt.strftime('%Y/%m/%d %H:%M:%S')
                    for dt in result_data[field]
                ]
            else:
                # 其他字段取整数
                result[field] = [round(float(val), 2) for val in result_data[field]]
        
        return result
        
    except Exception as e:
        logger.error(f"获取设备详情时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/device/history/{device_type}/{device_id}/fault_prob")
async def get_device_history(device_type: str, device_id: str):
    try:
        # 构建文件路径
        file_mapping = {
            'meter': 'water_meter_history.csv',
            'pipe': 'water_pipe_history.csv',
            'pump': 'water_pump_history.csv'
        }
        
        if device_type not in file_mapping:
            raise HTTPException(status_code=400, detail="Invalid device type")
            
        file_path = Path(__file__).parent.parent.parent / 'scripts' / 'data' / 'history' / file_mapping[device_type]
        
        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        # 筛选指定设备的数据
        device_data = df[df['device_id'] == device_id]
        
        if device_data.empty:
            raise HTTPException(status_code=404, detail=f"Device {device_id} not found")
        
        # 构建返回数据结构
        results = []
        for _, row in device_data.iterrows():
            timestamp = row['timestamp']
            fault_prob = row['fault_probability']
            
            results.append({
                "name": timestamp,
                "value": [
                    timestamp,
                    fault_prob
                ]
            })
        
        # 按时间戳排序
        results.sort(key=lambda x: x['name'])
        
        return {"results": results}
        
    except Exception as e:
        logger.error(f"获取设备历史数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# 定义每种设备可能的所有故障类型
FAULT_TYPES = {
    'meter': [
        '正常',
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
        '正常',
        '漏水',
        '堵塞',
        '腐蚀',
        '管道破裂',
        '水质问题'
    ],
    'pump': [
        '正常',
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

@router.get("/device/{device_type}/{device_id}/fault_pie")
async def get_device_fault_stats(device_type: str, device_id: str):
    try:
        # 验证设备类型
        if device_type not in FAULT_TYPES:
            raise HTTPException(status_code=400, detail="Invalid device type")
            
        # 构建文件路径
        file_mapping = {
            'meter': 'water_meter_history.csv',
            'pipe': 'water_pipe_history.csv',
            'pump': 'water_pump_history.csv'
        }
        
        file_path = Path(__file__).parent.parent.parent / 'scripts' / 'data' / 'history' / file_mapping[device_type]
        
        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        # 筛选指定设备的数据
        device_data = df[df['device_id'] == device_id]
        
        if device_data.empty:
            raise HTTPException(status_code=404, detail=f"Device {device_id} not found")
        
        # 统计故障类型数量
        fault_counts = device_data['fault_type'].value_counts().to_dict()
        
        # 构建包含所有可能故障类型的结果
        results = [
            {
                "name": fault_type,
                "value": fault_counts.get(fault_type, 0)  # 如果没有出现过该故障类型，返回0
            }
            for fault_type in FAULT_TYPES[device_type]
        ]
        
        # 按照数量降序排序
        results.sort(key=lambda x: x['value'], reverse=True)
        
        return {"results": results}
        
    except Exception as e:
        logger.error(f"获取设备故障统计时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



class DeviceData(BaseModel):
    data: dict

@router.post("/simulation/data")
async def save_device_data(request: DeviceData):
    try:
        device_data = request.data.copy()
        device_type = device_data.pop('device_type')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 定义每种设备类型需要的字段
        required_fields = {
            'water-meter': [
                'device_id', 'flux', 'pressure', 'signal', 
                'voltage', 'ph', 'turb', 'ozone', 'caliber'
            ],
            'water-pump': [
                'device_id', 'temp', 'shake', 'humidity', 
                'flux', 'power', 'noise', 'caliber'
            ],
            'water-pipe': [
                'device_id', 'pipe_stage', 'pipe_age', 'pipe_diameter',
                'pipe_length', 'pipe_pressure', 'flux', 'bury_depth', 'caliber'
            ]
        }
        
        if device_type not in required_fields:
            raise HTTPException(status_code=400, detail="Invalid device type")
            
        # 检查是否所有必需字段都存在
        missing_fields = [field for field in required_fields[device_type] 
                         if field not in device_data]
        if missing_fields:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        # 根据设备类型构建数据结构
        data_row = {'device_id': device_data['device_id'], 'timestamp': timestamp}
        
        if device_type == 'water-meter':
            data_row.update({
                'flux': device_data['flux'],
                'pressure': device_data['pressure'],
                'signal': device_data['signal'],
                'voltage': device_data['voltage'],
                'ph': device_data['ph'],
                'turb': device_data['turb'],
                'ozone': device_data['ozone'],
                'caliber': device_data['caliber']
            })
        elif device_type == 'water-pump':
            data_row.update({
                'temp': device_data['temp'],
                'shake': device_data['shake'],
                'humidity': device_data['humidity'],
                'flux': device_data['flux'],
                'power': device_data['power'],
                'noise': device_data['noise'],
                'caliber': device_data['caliber']
            })
        elif device_type == 'water-pipe':
            data_row.update({
                'pipe_stage': device_data['pipe_stage'],
                'pipe_age': device_data['pipe_age'],
                'pipe_diameter': device_data['pipe_diameter'],
                'pipe_length': device_data['pipe_length'],
                'pipe_pressure': device_data['pipe_pressure'],
                'flux': device_data['flux'],
                'bury_depth': device_data['bury_depth'],
                'caliber': device_data['caliber']
            })
        
        # 构建新数据行
        new_row = pd.DataFrame([data_row])
        
        # 构建文件路径
        file_mapping = {
            'water-meter': 'water_meter_test.csv',
            'water-pipe': 'water_pipe_test.csv',
            'water-pump': 'water_pump_test.csv'
        }
        
        file_path = Path(__file__).parent.parent.parent / 'scripts' / 'data' / 'logs' / file_mapping[device_type]
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 如果文件不存在，直接写入新数据
        if not file_path.exists():
            new_row.to_csv(file_path, index=False)
        else:
            df = pd.read_csv(file_path)
            if device_data['device_id'] in df['device_id'].values:
                df.loc[df['device_id'] == device_data['device_id']] = new_row.iloc[0]
            else:
                df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(file_path, index=False)
        
        return {
            "message": "数据保存成功",
            "device_type": device_type,
            "timestamp": timestamp
        }
        
    except KeyError as e:
        logger.error(f"保存设备数据时发生错误: 缺少必需字段 {str(e)}")
        raise HTTPException(status_code=400, detail=f"Missing required field: {str(e)}")
    except Exception as e:
        logger.error(f"保存设备数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))