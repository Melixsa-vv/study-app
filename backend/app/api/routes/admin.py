from fastapi import APIRouter, Depends, status
from app.api.deps import get_current_admin, get_db

from app.models.user import User
from app.services.admin_service import admin_service


router = APIRouter()

@router.delete("/session/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def hard_delete_session(
    *,
    db = Depends(get_db),
    session_id: int, 
    admin: User = Depends(get_current_admin),
):
    admin_service.hard_remove_session(db, session_id=session_id)