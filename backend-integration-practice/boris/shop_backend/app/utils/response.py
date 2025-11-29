from typing import Any, Mapping, Optional
from rest_framework import status
from rest_framework.response import Response

from .constants import ResponseCode, ResponseMessage


class APISuccessResponse(Response):
    """
    Unified success response:
    {
      "code": <int>,
      "msg": <str>,
      "data": <object | array | {} >
    }
    """
    def __init__(
        self,
        *,
        data: Any = None,
        code: int = ResponseCode.SUCCESS,
        msg: str = ResponseMessage.SUCCESS,
        status_code: int = status.HTTP_200_OK,
        headers: Optional[Mapping[str, str]] = None,
    ):
        payload = {
            "code": code,
            "msg": msg,
            "data": {} if data is None else data,
        }
        super().__init__(data=payload, status=status_code, headers=headers)


class APIFailedResponse(Response):
    """
    Unified error response:
    {
      "code": <int>,
      "msg": <str>,
      "details": <object | array | str | null>
    }
    """
    def __init__(
        self,
        *,
        code: int,
        msg: str,
        details: Any = None,
        status_code: int = status.HTTP_200_OK,
        headers: Optional[Mapping[str, str]] = None,
        **kwargs,
    ):
        payload = {
            "code": code,
            "msg": msg,
            "details": details,
        }
        super().__init__(data=payload, status=status_code, headers=headers)
