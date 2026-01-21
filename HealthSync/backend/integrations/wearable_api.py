import requests
from fastapi import APIRouter, HTTPException
from typing import List, Dict
import os

router = APIRouter()

class WearableAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.wearabledevice.com/v1"

    def fetch_data(self, endpoint: str) -> Dict:
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=response.status_code, detail=str(http_err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

@router.get("/wearable/data/{device_id}", response_model=Dict)
async def get_wearable_data(device_id: str):
    api_key = os.getenv("WEARABLE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")
    
    wearable_api = WearableAPI(api_key)
    data = wearable_api.fetch_data(f"devices/{device_id}/data")
    
    if not data:
        raise HTTPException(status_code=404, detail="No data found for the specified device")
    
    return data

@router.get("/wearable/devices", response_model=List[Dict])
async def list_wearable_devices():
    api_key = os.getenv("WEARABLE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")
    
    wearable_api = WearableAPI(api_key)
    devices = wearable_api.fetch_data("devices")
    
    if not devices:
        raise HTTPException(status_code=404, detail="No devices found")
    
    return devices