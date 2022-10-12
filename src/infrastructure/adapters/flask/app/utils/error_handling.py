from src.domain.entities.common_entity import ErrorEntity
from src.infrastructure.adapters.flask.app.utils.errors_definition import APIErrors


class AppErrorBaseClass(Exception):
    pass


class ObjectNotFound(AppErrorBaseClass):
    pass


class IntegrityErrorApp(AppErrorBaseClass):
    pass


class AuthError(AppErrorBaseClass):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


class TokenExpiredError(Exception):
    def __init__(self):
        self.status_code = 401
        self.error = {"code": "E2000",
                      "message": "token is expired",
                      "description": "token is expired. Refresh your token.",
                      "status_code": self.status_code
                      }


class AuthErrorBaseError(Exception):
    def __init__(self):
        self.dict_errors = {'TokenExpiredError': {"code": "E2000",
                                                  "message": "token is expired",
                                                  "description": "token is expired. Refresh your token.",
                                                  "status_code": 401},
                            'InvalidClaimsError': {"code": "E2001",
                                                  "message": "token is expired",
                                                  "description": "token is expired. Refresh your token.",
                                                  "status_code": 401},
                            }


def api_error(error_name):
    """Internal API error handler"""

    error = APIErrors[f"{error_name}"]

    res_error = ErrorEntity(
        status_code=error['error']["status_code"],
        error=error['error']
    )
    return res_error



