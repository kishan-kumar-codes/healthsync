from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, HealthData, Provider
from ..schemas import HealthDataShareRequest, HealthDataResponse
from ..security import get_current_user, verify_user_access
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/share_health_data", response_model=HealthDataResponse)
async def share_health_data(
    share_request: HealthDataShareRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Verify if the user has access to share the data
        if not verify_user_access(current_user, share_request.provider_id):
            raise HTTPException(status_code=403, detail="Access denied to share data with this provider.")

        # Fetch the health data for the user
        health_data = db.query(HealthData).filter(HealthData.user_id == current_user.id).first()
        if not health_data:
            raise HTTPException(status_code=404, detail="Health data not found.")

        # Share the health data with the specified provider
        provider = db.query(Provider).filter(Provider.id == share_request.provider_id).first()
        if not provider:
            raise HTTPException(status_code=404, detail="Provider not found.")

        # Logic to securely share data (e.g., encryption, logging)
        # Here we would implement the actual sharing mechanism
        # For example, encrypting the data before sending it
        encrypted_data = encrypt_health_data(health_data.data)

        # Log the sharing event
        logger.info(f"User {current_user.id} shared health data with provider {provider.id}")

        return HealthDataResponse(message="Health data shared successfully.", data=encrypted_data)

    except Exception as e:
        logger.error(f"Error sharing health data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")

def encrypt_health_data(data):
    # Placeholder for encryption logic
    return data  # Replace with actual encryption logic