from src.domain.entities.common_entity import ErrorEntity
from src.infrastructure.adapters.flask.app.utils.errors_definition import APIErrors


def api_error(error_name):
    """Internal API error handler"""

    error = APIErrors[f"{error_name}"]

    res_error = ErrorEntity(
        status_code=error['error']["status_code"],
        error=error['error']
    )
    return res_error



