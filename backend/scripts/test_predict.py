import pandas as pd
import json
import os
from device_fault_predictor import DeviceFaultPredictor
from datetime import datetime

def format_probability(prob: float) -> float:
    """将概率转换为百分比格式，保留2位小数"""
    return round(prob * 100, 2)

def get_status(prob: float) -> str:
    """根据故障概率确定状态"""
    if prob >= 70:  # 概率大于70%
        return "严重故障"
    elif prob >= 50:  # 概率大于50%
        return "故障"
    elif prob >= 30:  # 概率大于30%
        return "警告"
    return "正常"

def main():
    # 初始化预测器
    predictor = DeviceFaultPredictor()
    
    # 确保输出目录存在
    os.makedirs('output', exist_ok=True)
    
    # 获取当前时间作为预测批次标识
    batch_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 加载数据
    device_types = ['water_meter', 'water_pipe', 'water_pump']
    
    for device_type in device_types:
        try:
            # 加载训练数据
            train_data = pd.read_csv(f'data/sample/{device_type}_train.csv')
            
            # 训练模型
            print(f"训练 {device_type} 模型...")
            predictor.train(device_type, train_data)
            
            # 加载测试数据
            test_data = pd.read_csv(f'data/logs/{device_type}_test.csv')
            
            # 预测故障概率
            print(f"\n预测 {device_type} 故障...")
            probas, fault_types = predictor.predict_fault_probability(device_type, test_data)
            
            # 构建预测结果
            results = []
            for i, (prob, faults) in enumerate(zip(probas, fault_types)):
                prob_percentage = format_probability(prob)
                if prob_percentage >= 30:  # 保存故障概率超过30%的预测结果
                    result = {
                        'device_id': test_data.iloc[i]['device_id'],
                        'timestamp': test_data.iloc[i]['timestamp'],
                        'fault_probability': f"{prob_percentage}%",  # 添加百分号
                        'fault_types': faults if faults else [],
                        'status': get_status(prob_percentage),
                        'device_data': {  # 只保存关键设备数据
                            k: float(v) if isinstance(v, (int, float)) else v
                            for k, v in test_data.iloc[i].to_dict().items()
                            if k not in ['status', 'fault_type']  # 排除状态相关字段
                        }
                    }
                    results.append(result)
            
            # 按故障概率降序排序
            results.sort(key=lambda x: float(x['fault_probability'].rstrip('%')), reverse=True)
            
            # 保存预测结果到JSON文件
            output_file = f'output/{device_type}_prediction_{batch_time}.json'
            prediction_result = {
                'device_type': device_type,
                'prediction_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'summary': {
                    'total_devices': len(test_data),
                    'warning_devices': len(results),
                    'severe_fault_devices': sum(1 for r in results if r['status'] == "严重故障"),
                    'fault_devices': sum(1 for r in results if r['status'] == "故障"),
                    'warning_devices': sum(1 for r in results if r['status'] == "警告")
                },
                'predictions': results
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(prediction_result, f, ensure_ascii=False, indent=2)
            
            print(f"预测结果已保存到: {output_file}")
            print(f"检测到 {len(results)} 个异常设备")
            
            # 保存模型
            os.makedirs('models', exist_ok=True)
            predictor.save_model(f'models/{device_type}_model.pkl')
            
        except Exception as e:
            print(f"处理 {device_type} 时发生错误: {str(e)}")
            continue

if __name__ == "__main__":
    main()