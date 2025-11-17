from django.shortcuts import render
from rest_framework import viewsets
from .models import Temoignage
from .serializers import TemoignageSearilezer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from utils.supabase_client import upload_file


class TemoignageViewSet(viewsets.ModelViewSet):
    queryset = Temoignage.objects.all()
    serializer_class = TemoignageSearilezer
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


    @action(detail=False, methods=['get'], url_path='count/en_attente')
    def attente(self, request):
        temoignage = Temoignage.objects.filter(valide=False).count()
        #serializer = self.get_serializer(temoignage, many=True)
        return Response({'temoignage_en_attente' : temoignage })
    
    @action(detail=False, methods=['get'], url_path='en_attente')
    def attenteData(self, request):
        temoignage = Temoignage.objects.filter(valide=False)
        serializer = self.get_serializer(temoignage, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='count/valide')
    def valider(self, request):
        temoignage = Temoignage.objects.filter(valide=True).count()
        #serializer = self.get_serializer(temoignage, many=True)
        #return Response(serializer.data)
        return Response({'temoignage_valide': temoignage })
    
    @action(detail=False, methods=['get'], url_path='valide')
    def valideData(self, request):
        temoignage = Temoignage.objects.filter(valide=True)
        serializer = self.get_serializer(temoignage, many=True)
        return Response(serializer.data)
        #return Response({'temoignage_valide': temoignage })
    
    @action(detail=False, methods=['put, patch'], url_path='valider_temoin')
    def valider_temoignage(self, request):
        try:
            temoignage = self.get_object()
            temoignage.valide = True
            temoignage.save()

        except Exception as e :
           print("Erreur lors de la validation :", e)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)