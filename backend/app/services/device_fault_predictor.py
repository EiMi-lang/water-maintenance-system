import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from pyod.models.iforest import IForest
from pyod.models.knn import KNN
from pyod.models.lof import LOF
from typing import Dict, List, Tuple
import joblib

class DeviceFaultPredictor:
    def __init__(self):
        self.scalers = {}
        self.anomaly_models = {}
        self.fault_classifiers = {}  # 添加故障分类器
        
        # 定义每种设备的特征列
        self.feature_columns = {
            'water_meter': ['flux', 'pressure', 'signal', 'voltage', 'ph', 'turb', 'ozone', 'caliber'],
            'water_pipe': ['pipe_stage', 'pipe_age', 'pipe_diameter', 'pipe_length', 'pipe_pressure', 'flux', 'bury_depth', 'caliber'],
            'water_pump': ['temp', 'shake', 'humidity', 'flux', 'power', 'noise', 'caliber']
        }
        
        # 定义需要排除的列
        self.exclude_columns = ['device_id', 'timestamp', 'status', 'fault_type']
        
        # 定义参数正常范围
        self.normal_ranges = {
            'water_meter': {
                'flux': (0.1, 1000),
                'pressure': (0.1, 2.5),
                'signal': (-100, -70),
                'voltage': (6, 24),
                'ph': (6.5, 8.5),
                'turb': (0, 5),
                'ozone': (0, 0.1),
                'caliber': (15, 600)
            },
            'water_pipe': {
                'pipe_age': (0, 50),
                'pipe_diameter': (15, 600),
                'pipe_length': (1, 1000),
                'pipe_pressure': (0.1, 10.0),
                'flux': (0.5, 1000),
                'bury_depth': (1, 2),
                'caliber': (15, 600)
            },
            'water_pump': {
                'temp': (-10, 60),
                'shake': (10, 2000),
                'humidity': (20, 80),
                'flux': (1, 2000),
                'power': (0.5, 1000),
                'noise': (60, 90),
                'caliber': (15, 600)
            }
        }

    def prepare_features(self, df: pd.DataFrame, device_type: str) -> pd.DataFrame:
        """准备特征"""
        df = df.copy()
        
        # 选择特征列
        feature_cols = self.feature_columns[device_type]
        features_df = df[feature_cols].copy()
        
        # 添加时间特征
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            features_df['hour'] = df['timestamp'].dt.hour
            features_df['day'] = df['timestamp'].dt.day
            features_df['month'] = df['timestamp'].dt.month
            features_df['dayofweek'] = df['timestamp'].dt.dayofweek
        
        # 计算滚动统计特征
        for col in feature_cols:
            if col in df.columns:
                features_df[f'{col}_rolling_mean'] = df.groupby('device_id')[col].rolling(
                    window=3, min_periods=1).mean().reset_index(0, drop=True)
                features_df[f'{col}_rolling_std'] = df.groupby('device_id')[col].rolling(
                    window=3, min_periods=1).std().reset_index(0, drop=True)
        
        # 添加异常分数
        features_df['anomaly_score'] = df.apply(
            lambda row: self.calculate_anomaly_score(row, device_type), 
            axis=1
        )
        
        return features_df.fillna(0)

    def train(self, device_type: str, data: pd.DataFrame):
        """训练模型"""
        print(f"开始训练 {device_type} 模型...")
        print(f"原始数据形状: {data.shape}")
        
        # 准备特征
        features_df = self.prepare_features(data, device_type)
        print(f"处理后的特征: {features_df.columns.tolist()}")
        
        # 准备标签
        labels = (data['status'] != 'normal').astype(int)
        
        # 初始化标准化器
        self.scalers[device_type] = StandardScaler()
        scaled_data = self.scalers[device_type].fit_transform(features_df)
        
        # 训练异常检测模型集成
        self.anomaly_models[device_type] = {
            'iforest': IForest(contamination=0.2, random_state=42),
            'knn': KNN(contamination=0.2),
            'lof': LOF(contamination=0.2)
        }
        
        for name, model in self.anomaly_models[device_type].items():
            print(f"训练 {name} 模型...")
            model.fit(scaled_data)
        
        # 训练故障分类器
        self.fault_classifiers[device_type] = RandomForestClassifier(
            n_estimators=100, 
            random_state=42
        )
        
        # 使用异常样本训练故障分类器
        fault_mask = data['status'] != 'normal'
        if fault_mask.any():
            fault_features = features_df[fault_mask]
            fault_types = data[fault_mask]['fault_type']
            if not fault_types.isna().all():
                print("训练故障分类器...")
                self.fault_classifiers[device_type].fit(
                    self.scalers[device_type].transform(fault_features),
                    fault_types
                )

    def predict_fault_probability(self, device_type: str, data: pd.DataFrame) -> Tuple[np.ndarray, List[str]]:
        """预测故障概率并识别可能的故障类型"""
        # 准备特征
        features_df = self.prepare_features(data, device_type)
        scaled_data = self.scalers[device_type].transform(features_df)
        
        # 获取异常检测概率
        probas = []
        for model in self.anomaly_models[device_type].values():
            prob = model.predict_proba(scaled_data)[:, 1]
            probas.append(prob)
        
        # 计算平均概率
        avg_probas = np.mean(probas, axis=0)
        
        # 预测故障类型
        fault_types = []
        for i, prob in enumerate(avg_probas):
            if prob > 0.5:
                if device_type in self.fault_classifiers:
                    try:
                        fault_type = self.fault_classifiers[device_type].predict(
                            scaled_data[i:i+1]
                        )[0]
                        fault_types.append([fault_type])
                    except:
                        fault_types.append(self.identify_fault_types_by_rules(
                            data.iloc[i], 
                            device_type
                        ))
                else:
                    fault_types.append(self.identify_fault_types_by_rules(
                        data.iloc[i], 
                        device_type
                    ))
            else:
                fault_types.append([])
        
        return avg_probas, fault_types

    def identify_fault_types_by_rules(self, row: pd.Series, device_type: str) -> List[str]:
        """使用规则识别故障类型"""
        faults = []
        ranges = self.normal_ranges[device_type]
        
        if device_type == 'water_meter':
            if row['flux'] < ranges['flux'][0]:
                faults.extend(['堵塞', '泄漏', '传感器故障'])
            elif row['flux'] > ranges['flux'][1]:
                faults.extend(['电磁干扰', '水流冲击', '系统泄漏'])
                
            if row['pressure'] < ranges['pressure'][0]:
                faults.extend(['流量计量误差', '启动失败'])
            elif row['pressure'] > ranges['pressure'][1]:
                faults.extend(['设备损坏', '压力超限'])
                
        elif device_type == 'water_pipe':
            if row['pipe_pressure'] > ranges['pipe_pressure'][1]:
                faults.extend(['压力过高', '管道破裂风险'])
            if row['pipe_age'] > ranges['pipe_age'][1] * 0.8:
                faults.extend(['管道老化', '腐蚀风险'])
                
        elif device_type == 'water_pump':
            if row['temp'] > ranges['temp'][1]:
                faults.extend(['过热', '轴承损坏风险'])
            if row['shake'] > ranges['shake'][1]:
                faults.extend(['振动异常', '机械故障风险'])
            if row['noise'] > ranges['noise'][1]:
                faults.extend(['噪音异常', '机械磨损'])
                
        return list(set(faults))

    def calculate_anomaly_score(self, row: pd.Series, device_type: str) -> float:
        """计算异常分数"""
        score = 0
        ranges = self.normal_ranges[device_type]
        valid_fields = 0
        
        for field, (min_val, max_val) in ranges.items():
            if field in row.index:
                valid_fields += 1
                value = row[field]
                if value < min_val or value > max_val:
                    score += 1
                elif value < min_val * 1.1 or value > max_val * 0.9:
                    score += 0.5
                    
        return score / valid_fields if valid_fields > 0 else 1.0

    def save_model(self, path: str):
        """保存模型"""
        joblib.dump({
            'scalers': self.scalers,
            'anomaly_models': self.anomaly_models,
            'fault_classifiers': self.fault_classifiers,
            'normal_ranges': self.normal_ranges
        }, path)

    def load_model(self, path: str):
        """加载模型"""
        saved_data = joblib.load(path)
        self.scalers = saved_data['scalers']
        self.anomaly_models = saved_data['anomaly_models']
        self.fault_classifiers = saved_data['fault_classifiers']
        self.normal_ranges = saved_data['normal_ranges'] 