from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PresseSerializers
from .models import Presse
from rest_framework.permissions import AllowAny
from utils.supabase_client import upload_file


class PresseViewSet(viewsets.ModelViewSet):
    queryset = Presse.objects.all()
    serializer_class = PresseSerializers
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        file = request.FILES.get("image")  # Nom du champ dans le form
        if file:
            url = upload_file(file)
            request.data["image"] = url  # Remplace le fichier par l'URL Supabase
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        file = request.FILES.get("image")
        if file:
            url = upload_file(file)
            request.data["image"] = url
        return super().update(request, *args, **kwargs)

