from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    MethodNotAllowed,
    NotAuthenticated,
    PermissionDenied,
    ValidationError,
    NotFound,
    Throttled,
    ParseError,
)
from rest_framework.views import exception_handler as drf_exception_handler

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from .constants import ResponseCode, ResponseMessage
from .response import APIFailedResponse
from .exceptions import BusinessException

try:
    from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
except ImportError:
    InvalidToken = None
    TokenError = None


class ResponseFormatMixin:
    """Map DRF/JWT exceptions to your unified API envelope."""

    # ---- Handlers ----

    def handle_validation_error(self, exc, context):
        """處理驗證錯誤"""
        return APIFailedResponse(
            code=ResponseCode.VALIDATION_ERROR,
            msg=ResponseMessage.VALIDATION_ERROR,
            details=exc.detail,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def handle_method_not_allowed(self, exc, context):
        """處理MethodNotAllowed錯誤"""
        return APIFailedResponse(
            code=ResponseCode.METHOD_NOT_ALLOWED,
            msg=ResponseMessage.METHOD_NOT_ALLOWED,
            details=str(getattr(exc, "detail", "")) or None,
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def handle_not_found(self, exc, context):
        # 若要更細分「使用者不存在」，可在你的業務邏輯中主動回 USER_NOT_FOUND
        return APIFailedResponse(
            code=ResponseCode.NOT_FOUND,
            msg=ResponseMessage.NOT_FOUND,
            details=str(getattr(exc, "detail", "")) or None,
            status_code=status.HTTP_404_NOT_FOUND,
        )

    def handle_permission_denied(self, exc, context):
        # 優先使用 FORBIDDEN，備援 PERMISSION_DENIED
        code = getattr(ResponseCode, "FORBIDDEN", ResponseCode.PERMISSION_DENIED)
        msg = getattr(ResponseMessage, "FORBIDDEN", ResponseMessage.PERMISSION_DENIED)
        return APIFailedResponse(
            code=code,
            msg=msg,
            status_code=status.HTTP_403_FORBIDDEN,
        )

    def handle_not_authenticated(self, exc, context):
        return APIFailedResponse(
            code=ResponseCode.UNAUTHORIZED,
            msg=ResponseMessage.UNAUTHORIZED,
            details=str(getattr(exc, "detail", "")) or None,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    def handle_authentication_failed(self, exc, context):
        # 帳密錯、錯誤的 token 格式
        return APIFailedResponse(
            code=ResponseCode.INVALID_TOKEN,
            msg=ResponseMessage.INVALID_TOKEN,
            details=str(getattr(exc, "detail", "")) or None,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    def handle_throttled(self, exc, context):
        '''處理使用者重複操作、請求太多次'''
        retry_after = getattr(exc, "wait", None)
        headers = {"Retry-After": str(int(retry_after))} if retry_after else None
        return APIFailedResponse(
            code=getattr(ResponseCode, "RATE_LIMITED", ResponseCode.UNKNOWN_ERROR),
            msg=getattr(ResponseMessage, "RATE_LIMITED", ResponseMessage.UNKNOWN_ERROR),
            details={"retry_after": retry_after},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            headers=headers,
        )

    def handle_parse_error(self, exc, context):
        # JSON 解析等壞請求 → 以驗證錯誤代表 400
        return APIFailedResponse(
            code=ResponseCode.VALIDATION_ERROR,
            msg=ResponseMessage.VALIDATION_ERROR,
            details=str(getattr(exc, "detail", "")) or None,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def handle_jwt_error(self, exc, context):
        """
        simplejwt:
          - TokenError   → 常見於過期 → TOKEN_EXPIRED
          - InvalidToken → 簽章錯/結構錯 → INVALID_TOKEN
        """
        if TokenError and isinstance(exc, TokenError):
            code = getattr(ResponseCode, "TOKEN_EXPIRED", ResponseCode.UNAUTHORIZED)
            msg  = getattr(ResponseMessage, "TOKEN_EXPIRED", ResponseMessage.UNAUTHORIZED)
        else:
            code = getattr(ResponseCode, "INVALID_TOKEN", ResponseCode.UNAUTHORIZED)
            msg  = getattr(ResponseMessage, "INVALID_TOKEN", ResponseMessage.UNAUTHORIZED)

        detail = None
        if hasattr(exc, "detail") and exc.detail:
            detail = exc.detail.get("detail") if isinstance(exc.detail, dict) else str(exc.detail)

        return APIFailedResponse(
            code=code,
            msg=msg,
            details=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # ---- Entry point ----

    def handle_exception_service(self, exc, context):
        if isinstance(exc, ValidationError):
            return self.handle_validation_error(exc, context)

        if isinstance(exc, MethodNotAllowed):
            return self.handle_method_not_allowed(exc, context)

        if isinstance(exc, NotFound):
            return self.handle_not_found(exc, context)

        if isinstance(exc, PermissionDenied):
            return self.handle_permission_denied(exc, context)

        if isinstance(exc, NotAuthenticated):
            return self.handle_not_authenticated(exc, context)

        if isinstance(exc, AuthenticationFailed):
            return self.handle_authentication_failed(exc, context)

        if isinstance(exc, Throttled):
            return self.handle_throttled(exc, context)

        if isinstance(exc, ParseError):
            return self.handle_parse_error(exc, context)
        
        if isinstance(exc, (Http404, ObjectDoesNotExist)):
            '''將 Django 原生 404 對齊為統一格式'''
            return self.handle_not_found(exc, context)
        if isinstance(exc, BusinessException):
            '''處理商業邏輯相關的例外'''
            return APIFailedResponse(
            code=exc.code,
            msg=exc.msg,
            details=exc.details,
            status_code=exc.http_status,)

        # JWT
        if InvalidToken and isinstance(exc, InvalidToken):
            return self.handle_jwt_error(exc, context)
        if TokenError and isinstance(exc, TokenError):
            return self.handle_jwt_error(exc, context)

        # fallback to DRF default (keeps DRF's native shape for uncaught errors)
        return drf_exception_handler(exc, context)


def custom_exception_handler(exc, context):
    return ResponseFormatMixin().handle_exception_service(exc, context)
