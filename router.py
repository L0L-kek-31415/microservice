from fastapi import APIRouter
from service import get_statistics_for_page

router = APIRouter(
    responses={404: {"description": "Page not found"}}
)


@router.post('/statistics/{page_id}')
async def statistics(page_id: int):
    return get_statistics_for_page(page_id)