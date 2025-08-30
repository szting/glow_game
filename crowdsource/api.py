from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ..database.connection import get_db
from ..models.suggestion import ChallengeSuggestion
from ..models.user import User

router = APIRouter(prefix="/crowdsource", tags=["crowdsource"])

class ChallengeSubmission(BaseModel):
    title: str
    description: str
    color: str
    language: str = "en"
    user_telegram_id: int

class ChallengeSubmissionResponse(BaseModel):
    id: int
    title: str
    description: str
    color: str
    language: str
    status: str
    created_at: str

@router.post("/submit", response_model=ChallengeSubmissionResponse)
async def submit_challenge(
    submission: ChallengeSubmission,
    db: Session = Depends(get_db)
):
    """Submit a new challenge suggestion"""
    # Validate color
    valid_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    if submission.color not in valid_colors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid color. Must be one of: {', '.join(valid_colors)}"
        )
    
    # Validate language
    valid_languages = ['en', 'zh']
    if submission.language not in valid_languages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid language. Must be one of: {', '.join(valid_languages)}"
        )
    
    # Check if user exists
    user = db.query(User).filter(User.telegram_id == submission.user_telegram_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create suggestion
    suggestion = ChallengeSuggestion(
        user_id=user.id,
        title=submission.title,
        description=submission.description,
        color=submission.color,
        language=submission.language,
        status='pending'
    )
    
    db.add(suggestion)
    db.commit()
    db.refresh(suggestion)
    
    return ChallengeSubmissionResponse(
        id=suggestion.id,
        title=suggestion.title,
        description=suggestion.description,
        color=suggestion.color,
        language=suggestion.language,
        status=suggestion.status,
        created_at=suggestion.created_at.isoformat()
    )

@router.get("/suggestions", response_model=List[ChallengeSubmissionResponse])
async def get_suggestions(
    status: Optional[str] = None,
    color: Optional[str] = None,
    language: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get challenge suggestions with optional filtering"""
    query = db.query(ChallengeSuggestion)
    
    if status:
        query = query.filter(ChallengeSuggestion.status == status)
    if color:
        query = query.filter(ChallengeSuggestion.color == color)
    if language:
        query = query.filter(ChallengeSuggestion.language == language)
    
    suggestions = query.order_by(ChallengeSuggestion.created_at.desc()).all()
    
    return [
        ChallengeSubmissionResponse(
            id=s.id,
            title=s.title,
            description=s.description,
            color=s.color,
            language=s.language,
            status=s.status,
            created_at=s.created_at.isoformat()
        )
        for s in suggestions
    ]

@router.put("/suggestions/{suggestion_id}/status")
async def update_suggestion_status(
    suggestion_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update suggestion status (admin only)"""
    valid_statuses = ['pending', 'approved', 'rejected']
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    suggestion = db.query(ChallengeSuggestion).filter(
        ChallengeSuggestion.id == suggestion_id
    ).first()
    
    if not suggestion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suggestion not found"
        )
    
    suggestion.status = status
    db.commit()
    
    return {"message": f"Suggestion status updated to {status}"}
