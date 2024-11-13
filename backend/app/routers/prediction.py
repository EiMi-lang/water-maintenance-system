from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import pandas as pd
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from ..services.device_fault_predictor import DeviceFaultPredictor

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# 获取当前文件的目录
CURRENT_DIR = Path(__file__).parent.parent.parent  # 回到 backend 目录

def check_file_exists(file_path: str, file_type: str) -> None:
    """检查文件是否存在并可访问"""
    abs_path = os.path.abspath(file_path)
    logger.info(f"检查{file_type}文件路径: {abs_path}")
    
    if not os.path.exists(abs_path):
        error_msg = f"找不到{file_type}文件: {abs_path}"
        logger.error(error_msg)
        raise HTTPException(status_code=404, detail=error_msg)
    if not os.access(abs_path, os.R_OK):
        error_msg = f"无法读取{file_type}文件: {abs_path}"
        logger.error(error_msg)
        raise HTTPException(status_code=403, detail=error_msg)

@router.get("/predict/devices/faults")
async def predict_device_faults():
    """预测设备故障的端点"""
    try:
        logger.info("开始设备故障预测...")
        
        # 初始化预测器
        predictor = DeviceFaultPredictor()
        
        # 设备文件配置
        device_files = {
            'water_meter': {
                'test': str(CURRENT_DIR / 'scripts/data/logs/water_meter_test.csv'),
                'train': str(CURRENT_DIR / 'scripts/data/sample/water_meter_train.csv'),
                'model': str(CURRENT_DIR / 'water_meter_model.pkl')
            },
            'water_pipe': {
                'test': str(CURRENT_DIR / 'scripts/data/logs/water_pipe_test.csv'),
                'train': str(CURRENT_DIR / 'scripts/data/sample/water_pipe_train.csv'),
                'model': str(CURRENT_DIR / 'water_pipe_model.pkl')
            },
            'water_pump': {
                'test': str(CURRENT_DIR / 'scripts/data/logs/water_pump_test.csv'),
                'train': str(CURRENT_DIR / 'scripts/data/sample/water_pump_train.csv'),
                'model': str(CURRENT_DIR / 'water_pump_model.pkl')
            }
        }
        
        result = {
            'meterData': {},
            'pipeData': {},
            'pumpData': {}
        }
        
        for device_type, paths in device_files.items():
            try:
                logger.info(f"\n开始处理 {device_type}...")
                
                # 检查和加载数据
                check_file_exists(paths['test'], f"{device_type}测试数据")
                test_data = pd.read_csv(paths['test'])
                
                # 处理模型
                if os.path.exists(paths['model']):
                    predictor.load_model(paths['model'])
                else:
                    check_file_exists(paths['train'], f"{device_type}训练数据")
                    train_data = pd.read_csv(paths['train'])
                    predictor.train(device_type, train_data)
                    predictor.save_model(paths['model'])
                
                # 预测故障概率
                probas, fault_types = predictor.predict_fault_probability(device_type, test_data)
                
                # 构建预测结果
                predictions = []
                warning_count = 0
                severe_count = 0
                fault_count = 0
                
                for i, (prob, faults) in enumerate(zip(probas, fault_types)):
                    prob_percentage = round(prob * 100, 2)
                    if prob_percentage >= 30:  # 只包含异常数据
                        status = get_status(prob_percentage)
                        if status == "严重故障":
                            severe_count += 1
                        elif status == "故障":
                            fault_count += 1
                        
                    # 单独判断预警数量（概率大于75%）
                    if prob_percentage >= 75:
                        warning_count += 1
                        
                        # 根据设备类型构建不同的数据结构
                        device_data = test_data.iloc[i].to_dict()
                        prediction = {
                            'device_id': device_data['device_id'],
                            'timestamp': device_data['timestamp'],
                            'fault_probability': f"{prob_percentage}%",
                            'fault_types': faults[0] if faults else None  # 只取第一个故障类型
                        }
                        
                        # 添加设备特定的数据字段
                        if device_type == 'water_meter':
                            prediction.update({
                                'flux': round(device_data['flux'], 2),
                                'pressure': round(device_data['pressure'], 2),
                                'voltage': round(device_data['voltage'], 2),
                                'signal': device_data['signal'],
                                'ph': round(device_data['ph'], 2),
                                'turb': round(device_data['turb'], 2),
                                'ozone': round(device_data['ozone'], 3),
                                'caliber': device_data['caliber']
                            })
                        elif device_type == 'water_pipe':
                            prediction.update({
                                'pipe_stage': device_data['pipe_stage'],
                                'pipe_age': round(device_data['pipe_age'], 2),
                                'pipe_diameter': round(device_data['pipe_diameter'], 2),
                                'pipe_length': round(device_data['pipe_length'], 2),
                                'pipe_pressure': round(device_data['pipe_pressure'], 2),
                                'flux': round(device_data['flux'], 2),
                                'bury_depth': round(device_data['bury_depth'], 2),
                                'caliber': device_data['caliber']
                            })
                        elif device_type == 'water_pump':
                            prediction.update({
                                'temp': round(device_data['temp'], 2),
                                'shake': round(device_data['shake'], 2),
                                'humidity': round(device_data['humidity'], 2),
                                'flux': round(device_data['flux'], 2),
                                'power': device_data['power'],
                                'noise': round(device_data['noise'], 2),
                                'caliber': device_data['caliber']
                            })
                            
                        predictions.append(prediction)
                
                # 按故障概率降序排序
                predictions.sort(key=lambda x: float(x['fault_probability'].rstrip('%')), reverse=True)
                
                # 构建设备类型对应的数据结构
                device_data = {
                    'summary': {
                        'total_devices': len(test_data),
                        'warning_devices': warning_count,
                        'severe_fault_devices': severe_count,
                        'fault_devices': fault_count
                    },
                    'predictions': predictions
                }
                
                # 将数据添加到对应的键
                if device_type == 'water_meter':
                    result['meterData'] = device_data
                elif device_type == 'water_pipe':
                    result['pipeData'] = device_data
                elif device_type == 'water_pump':
                    result['pumpData'] = device_data
                
            except Exception as e:
                error_msg = f"处理{device_type}时发生错误: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise HTTPException(status_code=500, detail=error_msg)
        
        # 保存预测结果
        # batch_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        # output_file = str(CURRENT_DIR / f'devices_prediction_{batch_time}.json')
        # with open(output_file, 'w', encoding='utf-8') as f:
        #     json.dump(result, f, ensure_ascii=False, indent=2)
        
        return result
        
    except Exception as e:
        error_msg = f"预测过程发生错误: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

def get_status(prob: float) -> str:
    """根据故障概率确定状态"""
    if prob >= 70:
        return "严重故障"
    elif prob >= 50:
        return "故障"
    elif prob >= 30:
        return "警告"
    return "正常"