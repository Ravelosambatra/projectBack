from django.shortcuts import render
from rest_framework import viewsets
from .models import Projet
from .serializers import ProjetSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from utils.supabase_client import upload_file

class ProjetViewSet(viewsets.ModelViewSet):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print("🔹 Données reçues:", request.data)      # Affiche les données du POST
        print("🔹 Fichiers reçus:", request.FILES)     # Affiche les fichiers uploadés

        # Si un fichier image est présent, upload sur Supabase
        file = request.FILES.get("image")
        if file:
            url = upload_file(file)
            request.data["image"] = url 
        
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("❌ Erreurs de validation:", serializer.errors)  # Affiche les erreurs du serializer
            return Response(serializer.errors, status=400)         # Renvoie les erreurs en JSON
        

        self.perform_create(serializer)
        return Response(serializer.data, status=201)
    
    def update(self, request, *args, **kwargs):
        # Même principe pour la mise à jour
        file = request.FILES.get("image")
        if file:
            url = upload_file(file)
            request.data["image"] = url

        return super().update(request, *args, **kwargs)

