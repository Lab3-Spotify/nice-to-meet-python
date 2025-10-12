from dataclasses import dataclass
from rest_framework import status as http_status

@dataclass
class BusinessException(Exception):
    code: int
    msg: str
    details: dict | str | None = None
    http_status: int = http_status.HTTP_400_BAD_REQUEST # 應該是200