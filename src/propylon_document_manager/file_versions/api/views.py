from django.shortcuts import render

from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from ..models import FileVersion
from .serializers import FileVersionSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status
import logging
import os

logger = logging.getLogger(__name__)


class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()
    lookup_field = "id"

    def create(self, request, *args, **kwargs):
        logger.info("created is called: ")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Perform splitting logic and create folders
        url = serializer.validated_data['url']
        logger.info(f"URL: {url}")
        url_parts = url.split("/")
        url_parts = [part for part in url_parts if part]

        base_dir = '.'

        try:
            # Create folders based on URL parts
            folder_path = base_dir
            for part in url_parts:
                folder_path = os.path.join(folder_path, part)
                logger.info(f"folderPath: {folder_path}")
                os.makedirs(folder_path, exist_ok=True)

            # Proceed with creating the model instance
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
