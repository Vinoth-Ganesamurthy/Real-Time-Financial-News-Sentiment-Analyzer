from fastapi import APIRouter, HTTPException

from src.services.company_service import get_stock_symbol
from src.services.stock_service import fetch_stock_quote


router = APIRouter(
    prefix="/stock",
    tags=["Stock Market"],
)


@router.get("/{company}")
def get_stock(company: str):

    symbol = get_stock_symbol(company)

    if symbol is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found."
        )

    try:
        quote = fetch_stock_quote(symbol)

        if quote["current_price"] is None:
            raise HTTPException(
                status_code=404,
                detail="Stock quote not available."
            )

        return {
            "company": company,
            **quote,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to fetch stock data: {str(e)}"
        )