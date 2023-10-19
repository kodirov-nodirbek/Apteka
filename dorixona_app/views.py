from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response


from . import serializers
from .models import (Apteka, Firma, FirmaSavdolari, Nasiyachi, Nasiya, KunlikSavdo, Bolim, HisoblanganOylik, Harajat)


class AptekaViewSet(ModelViewSet):
    queryset = Apteka.objects.all()
    serializer_class = serializers.AptekaSerializer
 
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class FirmaViewSet(ModelViewSet):
    queryset = Firma.objects.all()
    serializer_class = serializers.FirmaSerializer
 
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'masul_shaxs', 'phone', 'eng_yaqin_tolov_sanasi']
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class FirmaSavdolariViewSet(ModelViewSet):
    serializer_class = serializers.FirmaSavdolariSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['shartnoma_raqami', 'harid_sanasi', 'tolov_muddati']

    def get_queryset(self):
        queryset = FirmaSavdolari.objects.all().order_by("tolov_muddati")
        firma_id = self.request.query_params.get('firma_id')
        shartnoma_raqami = self.request.query_params.get('shartnoma_raqami')
        if firma_id and shartnoma_raqami:
            queryset = queryset.filter(firma_id=firma_id, shartnoma_raqami=shartnoma_raqami)
        elif firma_id:
            queryset = queryset.filter(firma_id=firma_id)
        elif shartnoma_raqami:
            queryset = queryset.filter(shartnoma_raqami=shartnoma_raqami)

        return queryset

    def update(self, request, *args, **kwargs):
        
        return super().update(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     savdo = request.data
    #     serializer = serializers.FirmaSavdolariSerializer(data=savdo)
    #     serializer.is_valid(raise_exception=True)
    #     valid_data = serializer.validated_data
    #     output = {**serializer.data}
    #     print(valid_data)
    #     return Response(output, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()
        instance = serializer.instance
        serializer.add_payment(instance, serializer.validated_data)

# class FirmaSavdolariTolovView(APIView):
#     def post(self, request):
#         firma_savdolari = FirmaSavdolari.objects.all()
#         serializer = serializers.FirmaSerializer(firma_savdolari, many=True)

class NasiyachiViewSet(ModelViewSet):
    queryset = Nasiyachi.objects.all()
    serializer_class = serializers.NasiyachiSerializer
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'middle_name', 'phone', 'passport']

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    

class NasiyaViewSet(ModelViewSet):
    queryset = Nasiya.objects.all()
    serializer_class = serializers.NasiyaSerializer
 
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Nasiya.objects.all()
        nasiyachi_id = self.request.query_params.get('nasiyachi_id')
        if nasiyachi_id:
            queryset = queryset.filter(nasiyachi_id=nasiyachi_id)
        return queryset
    
class KunlikSavdoViewSet(ModelViewSet):
    queryset = KunlikSavdo.objects.all()
    serializer_class = serializers.KunlikSavdoSerializer
 
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class BolimViewSet(ModelViewSet):
    queryset = Bolim.objects.all()
    serializer_class = serializers.BolimSerializer
 
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class HisoblanganOylikViewSet(ModelViewSet):
    queryset = HisoblanganOylik.objects.all()
    serializer_class = serializers.HisoblanganOylikSerializer
 
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class HarajatViewSet(ModelViewSet):
    queryset = Harajat.objects.all()
    serializer_class = serializers.HarajatSerializer
 
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class HozirgiSana(APIView):
    def get(self, request):
        today = datetime.today()
        d = {
            "sana": str(today)[:10],
            "soat": str(today)[11:13],
            "daqiqa": str(today)[14:16]
        }
        return Response(d)