from fastapi import APIRouter, HTTPException
import pandas as pd
from pathlib import Path
import logging
from app.models.rag_model import generate_rag_response

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/device/rag/{device_desc}")
async def get_device_analysis(device_desc: str):
    try:
        prompt = f"""你是一个水务专家，基于你对不同种类设备的了解，请根据以下描述：{device_desc}，对当前设备的状态进行一个精准的总结和分析，并对接近临界值的参数给出预警,总字数控制在250字以内，
        去掉不必要的换行和缩进，例如，可以仿照以下格式输出，这只是个例子，不要完全照搬,不同的设备可能会有不同的字段，但是格式要仿照这个例子：
        根据提供的监控指标数据，水表设备WM_019存在严重故障的可能性高达85.03%，主要故障类型为"误读"。具体参数分析如下：
        1. 流量：6.92 m³/h，位于中口径水表范围内，正常。
        2. 压力：0.35 MPa，在小口径水表范围内，正常。
        3. 电压：6.05V，接近小口径水表的电压下限，存在电压过低故障风险。
        4. 信号强度：-79 dBm，位于正常范围内，正常。
        5. 酸碱度：7.81，正常范围内，正常。
        6. 浊度：2.76 NTU，正常范围内，正常。
        7. 臭氧：0.08 mg/L，正常范围内，正常。
        8. 口径：100，属于中口径水表。
        预警：需要立即关注电压参数，确保电池电量充足，避免电压过低故障。同时，对于误读故障，需要进一步检查和维护水表，以确保准确计量。建议及时进行维护和调整，以避免可能的故障发生。
        """
        response = generate_rag_response(prompt)
        return response
        
    except Exception as e:
        logger.error(f"获取设备数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/device/maintain/{device_desc}")
async def get_device_maintain(device_desc: str):
    try:
        prompt = f"""你是一个水务专家，基于你对不同种类设备的了解，请根据以下描述：{device_desc}，对当前设备故障(fault_type)给出专业的维护建议，总字数控制在250字以内,去掉不必要的换行符,不用
        输出其他的字段内容，只用针对故障类型输出维护建议，格式清晰，阅读性高。"""
        response = generate_rag_response(prompt)
        return response
        
    except Exception as e:
        logger.error(f"获取设备数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))