from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.dashboard_service import DashboardService
from app.schemas.dashboard import DashboardSummary
from app.models.user import User
from app.permissions.guards import get_current_analyst_or_admin

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
dashboard_service = DashboardService()


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_analyst_or_admin)
):
    return dashboard_service.get_summary(db, current_user.id)



