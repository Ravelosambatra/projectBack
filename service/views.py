from django.shortcuts import render
from .models import Service, Categorie
from .serializers import ServiceSerializer, CategorieSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from utils.supabase_client import upload_file

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [AllowAny]

    #uploder un image
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

    @action(detail=False, methods=['get'], url_path='with_commande')
    def commande(self, request):
        categories = Categorie.objects.filter(button__iexact = "Commander")
        serialiezer = self.get_serializer(categories, many=True)
        return Response(serialiezer.data)
    
    @action(detail=False, methods=['get'], url_path='with_inscription')
    def inscription(self, request):
        categories = Categorie.objects.filter(button__iexact = "S'inscrire")
        serialiezer = self.get_serializer(categories, many=True)
        return Response(serialiezer.data)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

    #uploder un image
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


    @action(detail=False, methods=['get'], url_path='by_categorie/(?P<categorie_id>[^/.]+)')
    def by_categorie(self, request, categorie_id=None):
        """categorie_id = request.query_params.get('categorie_id')
        if not categorie_id:
            return Response({"error":"categorie_id est requis"}, status=400)
        offres = self.queryset.filter(categorie_id=categorie_id)"""
        offres = Service.objects.filter(categorie_id=categorie_id)
        serializer = self.get_serializer(offres, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='count')
    def total(self, request):
        nb_total = Service.objects.count()
        return Response({'total_services': nb_total})
    
    @action(detail=False, methods=['get'], url_path='with_inscription')
    def avec_inscription(self, request):
        offres = Service.objects.filter(button__iexact="S'inscrire")
        serializer = self.get_serializer(offres, many=True)
        return Response(serializer.data)

