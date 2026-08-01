from fastapi import APIRouter

router = APIRouter(
    prefix="/news",
    tags=["Financial News"]
)

@router.get("/{company}")
def get_news(company: str):

    return {
        "company": company,
        "message": "API working successfully"
    }