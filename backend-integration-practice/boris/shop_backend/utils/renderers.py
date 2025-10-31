from rest_framework import status
from rest_framework.renderers import JSONRenderer

from utils.constants import ResponseCode, ResponseMessage
from utils.response import APIFailedResponse, APISuccessResponse


class ShopRenderer(JSONRenderer):
    """
    - 成功(<400)：自動包成 APISuccessResponse；保留原本 2xx（200/201/204...）
    - 失敗(>=400)：包成 APIFailedResponse，但保留 4xx/5xx
    - 若 data 已包含 'code'（表示已包成統一格式）→ 直接通過，不再重包、不改 HTTP
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not renderer_context:
            return super().render(data, accepted_media_type, renderer_context)

        response = renderer_context.get("response")
        if not response:
            return super().render(data, accepted_media_type, renderer_context)

        # 直接通過
        if isinstance(data, dict) and "code" in data:
            return super().render(data, accepted_media_type, renderer_context)

        status_code = response.status_code
        is_success = status_code < 400

        if is_success:
            # 成功：自動包裝但保持原本 2xx
            success = APISuccessResponse(
                data=data,
                code=ResponseCode.SUCCESS,
                msg=ResponseMessage.SUCCESS,
                status_code=status_code,
            )
            return super().render(success.data, accepted_media_type, renderer_context)

        # 失敗：包裝錯誤，保留原本 4xx/5xx
        failed = APIFailedResponse(
            code=self._map_status_to_code(status_code),
            msg=self._get_error_message(status_code, data),
            details=self._format_errors(data),
            status_code=status_code,
        )
        return super().render(failed.data, accepted_media_type, renderer_context)

    def _get_error_message(self, status_code, data):
        if status_code == status.HTTP_400_BAD_REQUEST:
            return ResponseMessage.VALIDATION_ERROR
        elif status_code == status.HTTP_401_UNAUTHORIZED:
            return ResponseMessage.UNAUTHORIZED
        elif status_code == status.HTTP_403_FORBIDDEN:
            return ResponseMessage.FORBIDDEN
        elif status_code == status.HTTP_404_NOT_FOUND:
            return ResponseMessage.NOT_FOUND
        elif status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            return ResponseMessage.METHOD_NOT_ALLOWED
        elif status_code == status.HTTP_409_CONFLICT:
            return ResponseMessage.CONFLICT
        elif status_code >= 500:
            return ResponseMessage.INTERNAL_ERROR

        # 從 data 嘗試取訊息
        if isinstance(data, dict):
            if "detail" in data:
                return data["detail"]
            elif "message" in data:
                return data["message"]
        return ResponseMessage.UNKNOWN_ERROR

    def _map_status_to_code(self, status_code):
        mapping = {
            status.HTTP_400_BAD_REQUEST: ResponseCode.VALIDATION_ERROR,
            status.HTTP_401_UNAUTHORIZED: ResponseCode.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: ResponseCode.FORBIDDEN,
            status.HTTP_404_NOT_FOUND: ResponseCode.NOT_FOUND,
            status.HTTP_405_METHOD_NOT_ALLOWED: ResponseCode.METHOD_NOT_ALLOWED,
            status.HTTP_409_CONFLICT: ResponseCode.CONFLICT,
            status.HTTP_500_INTERNAL_SERVER_ERROR: ResponseCode.INTERNAL_ERROR,
        }
        return mapping.get(status_code, ResponseCode.UNKNOWN_ERROR)

    def _format_errors(self, data):
        if isinstance(data, dict):
            # Serializer 欄位錯：{'field': ['msg', ...]}
            if any(isinstance(v, list) for v in data.values()):
                return data
            # 單一錯誤訊息：{'detail': '...'} / {'message': '...'}
            elif "detail" in data or "message" in data:
                return None
        elif isinstance(data, list):
            return {"non_field_errors": data}
        return data if data else None
