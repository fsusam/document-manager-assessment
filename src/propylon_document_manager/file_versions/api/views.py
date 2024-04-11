from django.shortcuts import render

from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from django.db.models import Max

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
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

         # get the file from the request
        file = request.FILES['file']
        # get the filename from the uploaded file
        file_name = file.name
        logger.info(f"uploaded file name: {file_name}")

        # get the file name by url
        url = request.data['url']

        # set home directory if the url is not defined
        if url == '':
            url = '/'

        try:
            # log the filtered queryset
            logger.info(f"url: {url} and file_name: {file_name}")
            logger.info(f"queryset: { len(self.queryset) }")
            logger.info(f"filtered queryset: { len(self.queryset.filter(url=url, file_name=file_name).all()) }")
            
            max_version_number = self.queryset.filter(url=url, file_name=file_name).aggregate(max_version_number=Max('version_number'))['max_version_number']
            logger.info(f"max_version_number: {max_version_number}")
            if max_version_number is None:
                # throw an error FileVersion.DoesNotExist if max_version_number is None
                logger.info("throw FileVersion.DoesNotExist")
                raise FileVersion.DoesNotExist
            
            next_version_number = max_version_number + 1
            # get the file name without the extension and extension separately
            # splitted file name
            splitted_file_name = file_name.split('.')            
            file_name_without_extension = file_name.split('.')[0]
            file_name_extension = '.'+splitted_file_name[1] if len(splitted_file_name) > 1 else ''
            
            
            new_file_name = file_name_without_extension+'_'+str(next_version_number)+file_name_extension

            file.name = new_file_name
            # create a new instance with the provided data
            file_version_obj = FileVersion.objects.create(
                url=url,
                file_name=file_name,
                file=file,
                version_number=next_version_number
            )
        except FileVersion.DoesNotExist:
            logger.info("FileVersion.DoesNotExist")
            # create a new instance with the provided data
            file_version_obj = FileVersion.objects.create(
                url=url,
                file_name=file_name,
                file=file

            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
