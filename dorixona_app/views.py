from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import filters, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
import json


from . import serializers
from .models import (Apteka, Firma, FirmaSavdolari, Nasiyachi, Nasiya, KunlikSavdo, Bolim, Hodim, HisoblanganOylik, Harajat, TovarYuborishFilial)


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
    search_fields = ['name', 'masul_shaxs', 'phone']
    
    def get_queryset(self):
        queryset = Firma.objects.all()
        firma_id = self.request.query_params.get('id')
        if firma_id:
            queryset = queryset.filter(firma_id=firma_id)
        
        return queryset

    def partial_update(self, request, *args, **kwargs):
        firma_object = self.get_object()
        savdolar = [savdo for savdo in FirmaSavdolari.objects.filter(firma_id=firma_object.id).order_by("tolov_muddati") if savdo.tolandi()==False]
        data = request.data
        tolov = data.get("tolov", None)
        apteka_id = data.get("apteka_id", None)
        for savdo in savdolar:
            if tolov and apteka_id and savdo.jami_qarz()>=tolov:
                pay = {
                    "summa": int(tolov),
                    'sana': str(datetime.now()),
                    'apteka_id': apteka_id
                }
                savdo.tolangan_summalar.append(pay)
                savdo.save()
                break
            elif tolov and apteka_id and savdo.jami_qarz()<tolov:
                pay = {
                    "summa": int(savdo.jami_qarz()),
                    'sana': str(datetime.now()),
                    'apteka_id': apteka_id
                }
                tolov-=savdo.jami_qarz()
                savdo.tolangan_summalar.append(pay)
                savdo.save()

        firma_object.name = data.get("name", firma_object.name)
        firma_object.masul_shaxs = data.get("masul_shaxs", firma_object.masul_shaxs)
        firma_object.phone = data.get("phone", firma_object.phone)

        firma_object.save()

        serializer = serializers.FirmaSerializer(firma_object)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

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

    def perform_create(self, serializer):
        serializer.save()
        instance = serializer.instance
        serializer.add_payment(instance, serializer.validated_data)


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

class HodimViewSet(ModelViewSet):
    queryset = Hodim.objects.all()
    serializer_class = serializers.HodimSerializer

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


class TovarYuborishFilialViewSet(ModelViewSet):
    queryset = TovarYuborishFilial.objects.all()
    serializer_class = serializers.TovarYuborishFilialSerializer


class HozirgiSana(APIView):
    def get(self, request):
        today = datetime.today()
        d = {
            "sana": str(today)[:10],
            "soat": str(today)[11:13],
            "daqiqa": str(today)[14:16]
        }
        return Response(d)
