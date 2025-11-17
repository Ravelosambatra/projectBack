from django.shortcuts import render
from rest_framework import viewsets
from .models import Blog
from .serializers import BlogSerializer
from rest_framework.permissions import AllowAny
from utils.supabase_client import upload_file

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        file = request.FILES.get("imageActu")  # Nom du champ dans le form
        if file:
            url = upload_file(file)
            request.data["imageActu"] = url  # Remplace le fichier par l'URL Supabase
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        file = request.FILES.get("imageActu")
        if file:
            url = upload_file(file)
            request.data["imageActu"] = url
        return super().update(request, *args, **kwargs)
