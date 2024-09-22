import logging
from ctrl.sample_ctrl import get_order_data
from fastapi import APIRouter, Request
from fastapi.responses import ORJSONResponse
from util.custom_exceptions import CustomException


logger = logging.getLogger(__name__)
router = APIRouter()


#TODO: Replace placeholder
@router.get('/',
            response_class=ORJSONResponse,
            status_code=200,
            description='Sample GET endpoint')
async def sample_get(
    req: Request
):
    logger.info(f'GET {req.url}, params={req.query_params}, body={await req.body()}')
    #add permissions check

    try:
        results = get_order_data()

    except CustomException as err:
        logger.error(str(err))
        raise CustomException(str(err), err.status_code)

    response = ORJSONResponse(results)

    return response
