from fastapi import APIRouter, HTTPException
from app.services.device_service import DeviceService

router = APIRouter()

@router.get("/devices/{device_type}")
async def get_devices(device_type: str):
    device_service = DeviceService()
    return device_service.get_device_list(device_type)

@router.get("/devices/{device_type}/{device_id}/history")
async def get_device_history(device_type: str, device_id: str, time_range: str = '24h'):
    device_service = DeviceService()
    return device_service.get_device_history(device_type, device_id, time_range)

@router.get("/devices/stats")
async def get_devices_stats():
    device_service = DeviceService()
    return device_service.get_device_stats() 