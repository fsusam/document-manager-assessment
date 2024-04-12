from django.http import FileResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from django.db.models import Max
from rest_framework import views

from propylon_document_manager.site.settings import base

from ..models import FileVersion
from .serializers import FileVersionSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import BaseAuthentication
import logging
import os

logger = logging.getLogger(__name__)


class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes=[]
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()
    lookup_field = "id"

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

         # get the file from the request
        file = request.FILES['file']
        
        # get the filename from the uploaded file
        file_name = file.name
        
        # get the file name by url
        url = request.data['url']

        logger.info(f"url: {url} and file_name: {file_name}")

        try:    
            max_version_number = self.queryset.filter(url=url, file_name=file_name).aggregate(max_version_number=Max('version_number'))['max_version_number']
            logger.info(f"max_version_number: {max_version_number}")
            if max_version_number is None:
                # throw an error FileVersion.DoesNotExist if max_version_number is None
                logger.info("throw FileVersion.DoesNotExist")
                raise FileVersion.DoesNotExist
            
            next_version_number = max_version_number + 1
            file.name = self.split_file_name(file_name, next_version_number)
            relative_url = url + file_name
            # create a new instance with the provided data
            file_version_obj = FileVersion.objects.create(
                url=url,
                relative_url= relative_url,
                file_name=file_name,
                file=file,
                version_number=next_version_number
            )
        except FileVersion.DoesNotExist:
            logger.info("FileVersion.DoesNotExist")
            file.name = self.split_file_name(file_name, 0)
            relative_url = url + file_name
            logger.info(f"relative_url: {relative_url} and url: {url} and file.name: {file.name} and file_name {file_name}")

            # create a new instance with the provided data
            file_version_obj = FileVersion.objects.create(
                url=url,
                relative_url= relative_url,
                file_name=file_name,
                file=file,
                version_number=0
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # create a function to split the file name and add the version number
    def split_file_name(self, file_name, version):
        splitted_file_name = file_name.split('.')            
        file_name_without_extension = splitted_file_name[0]
        file_name_extension = '.'+splitted_file_name[1] if len(splitted_file_name) > 1 else ''
        logger.info(f"new name: {file_name_without_extension + '_' + str(version) + file_name_extension}")
        return file_name_without_extension + '_' + str(version) + file_name_extension

class MediaFileView(views.APIView):
    authentication_classes = []
    permission_classes=[]
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()
    lookup_field = "id"

    def get(self, request, path, format=None):
        """
        Return a list of all users.
        """
        logger.info('relative url path: ' + path)
        revision = request.query_params.get('revision', 0)
        logger.info('revision: ' + revision)
        file_version = self.queryset.get(relative_url=path, version_number=revision)
        logger.info('file_version: ' + file_version.file_name)
        response = HttpResponse(file_version.file, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{file_version.file.name}"'
        return response
       