from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import status

from utils.renderers import ShopRenderer
from utils.response import APISuccessResponse
from utils.constants import ResponseCode, ResponseMessage

class BaseAPIView(APIView):
    renderer_classes = [ShopRenderer]


class BaseGenericViewSet(GenericViewSet):
    renderer_classes = [ShopRenderer]

