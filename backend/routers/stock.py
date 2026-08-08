from fastapi import APIRouter, HTTPException

from src.services.company_service import get_stock_symbol
from src.services.historical_stock_service import (
    fetch_historical_data,
    calculate_performance,
)

router = APIRouter(
    prefix="/stock",
    tags=["Stock Performance"],
)


@router.get("/performance/{company}")
def get_stock_performance(company: str):

    symbol = get_stock_symbol(company)

    if symbol is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found."
        )

    historical_data = fetch_historical_data(symbol)

    if not historical_data:
        raise HTTPException(
            status_code=404,
            detail="Historical stock data not found."
        )

    performance = calculate_performance(historical_data)

    if not performance:
        raise HTTPException(
            status_code=404,
            detail="Unable to calculate stock performance."
        )

    return {
        "company": company.title(),
        "symbol": symbol,
        **performance,
    }