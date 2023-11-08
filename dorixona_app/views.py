from datetime import datetime, timedelta
from rest_framework import filters, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .filters import TopshirilganPulFilter, KunlikSavdoFilter, FirmaSavdolariFilter, NasiyachiFilter, NasiyaFilter, HarajatFilter, TovarYuborishFilialFilter
from . import serializers
from .models import (Apteka, Firma, FirmaSavdolari, Nasiyachi, Nasiya, KunlikSavdo, TopshirilganPul, Bolim, BolimgaDori, Hodim, HisoblanganOylik, Harajat, TovarYuborishFilial)


class AptekaViewSet(ModelViewSet):
    queryset = Apteka.objects.all()
    serializer_class = serializers.AptekaSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class FirmaViewSet(ModelViewSet):
    queryset = Firma.objects.all()
    serializer_class = serializers.FirmaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'masul_shaxs', 'phone']
    

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
    queryset = FirmaSavdolari.objects.all()
    serializer_class = serializers.FirmaSavdolariSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FirmaSavdolariFilter

    def perform_create(self, serializer):
        serializer.save()
        instance = serializer.instance
        serializer.add_payment(instance, serializer.validated_data)


class NasiyachiViewSet(ModelViewSet):
    queryset = Nasiyachi.objects.all()
    serializer_class = serializers.NasiyachiSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = NasiyachiFilter
    search_fields = ['first_name', 'last_name', 'passport', 'phone', 'chek_raqami']
    

class NasiyaViewSet(ModelViewSet):
    queryset = Nasiya.objects.all().order_by('tolov_muddati')
    serializer_class = serializers.NasiyaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = NasiyaFilter
    search_fields = ['']

    
class KunlikSavdoViewSet(ModelViewSet):
    queryset = KunlikSavdo.objects.all()
    serializer_class = serializers.KunlikSavdoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = KunlikSavdoFilter
    

class BolimViewSet(ModelViewSet):
    queryset = Bolim.objects.all()
    serializer_class = serializers.BolimSerializer
    permission_classes = [IsAuthenticated]


class BolimgaDoriViewSet(ModelViewSet):
    queryset = BolimgaDori.objects.all()
    serializer_class = serializers.BolimgaDoriSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class HodimViewSet(ModelViewSet):
    queryset = Hodim.objects.all()
    serializer_class = serializers.HodimSerializer
    permission_classes = [IsAuthenticated]


class HisoblanganOylikViewSet(ModelViewSet):
    queryset = HisoblanganOylik.objects.all()
    serializer_class = serializers.HisoblanganOylikSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    
class HarajatViewSet(ModelViewSet):
    queryset = Harajat.objects.all()
    serializer_class = serializers.HarajatSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HarajatFilter


class TovarYuborishFilialViewSet(ModelViewSet):
    queryset = TovarYuborishFilial.objects.all()
    serializer_class = serializers.TovarYuborishFilialSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TovarYuborishFilialFilter
    
    def get_name(self):
        return self.name
    

class TopshirilganPulViewSet(ModelViewSet):
    queryset = TopshirilganPul.objects.all().order_by('-date')
    serializer_class = serializers.TopshirilganPulSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TopshirilganPulFilter


class HozirgiSana(APIView):
    def get(self, request):
        today = datetime.today()
        d = {
            "sana": str(today)[:10],
            "soat": str(today)[11:13],
            "daqiqa": str(today)[14:16]
        }
        return Response(d)