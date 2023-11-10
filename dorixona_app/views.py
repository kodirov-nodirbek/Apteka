from datetime import datetime
from rest_framework import filters, status, generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .filters import KunlikSavdoFilter, FirmaSavdolariFilter, NasiyachiFilter, NasiyaFilter, HarajatFilter, TovarYuborishFilialFilter, BolimgaDoriFilter, HisoblanganOylikFilter
from . import serializers
from .models import (Apteka, Firma, FirmaSavdolari, Nasiyachi, Nasiya, KunlikSavdo, Bolim, BolimgaDori, Hodim, HisoblanganOylik, Harajat, TovarYuborishFilial, KirimDorilar, OlinganOylik)


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
        naqd = data.get("naqd", 0)
        plastik = data.get("plastik", 0)
        apteka_id = data.get("apteka_id", None)
        tolov = naqd+plastik
        print("naqd", naqd)
        print("plastik", plastik)
        print('jami', tolov)
        for savdo in savdolar:
            if tolov!=0 and apteka_id and savdo.jami_qarz()>=tolov:
                pay = {
                    "summa": int(tolov),
                    'sana': str(datetime.now()),
                    'apteka_id': apteka_id
                }
                savdo.tolangan_summalar.append(pay)
                savdo.save()
                break
            elif tolov!=0 and apteka_id and savdo.jami_qarz()<tolov:
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
        if apteka_id and tolov!=0:
            Harajat.objects.create(apteka_id=Apteka.objects.get(id=apteka_id), naqd_pul=naqd, plastik=plastik, firma_uchun=True, izoh=f"{firma_object.id}, '{firma_object.name}' firmasi uchun")
        serializer = serializers.FirmaSerializer(firma_object)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class FirmaSavdolariViewSet(ModelViewSet):
    queryset = FirmaSavdolari.objects.all()
    serializer_class = serializers.FirmaSavdolariSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FirmaSavdolariFilter

    # def perform_create(self, serializer):
    #     serializer.save()
    #     instance = serializer.instance
    #     serializer.add_payment(instance, serializer.validated_data)


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
    filter_backends = [DjangoFilterBackend]
    filterset_class = NasiyaFilter
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # search_fields = ['']

    
class KunlikSavdoViewSet(ModelViewSet):
    queryset = KunlikSavdo.objects.all().order_by('-date')
    serializer_class = serializers.KunlikSavdoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = KunlikSavdoFilter
    

class KunlikSavdoUpdateView(generics.UpdateAPIView):
    queryset = KunlikSavdo.objects.all()
    serializer_class = serializers.KunlikSavdoSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        
        id_list = request.data.get('id_list', [])
        
        instances = self.get_queryset().filter(id__in=id_list)
        
        for instance in instances:
            instance.qabul_qildi = True
            instance.save()

        return Response(status=status.HTTP_200_OK)


class BolimViewSet(ModelViewSet):
    queryset = Bolim.objects.all()
    serializer_class = serializers.BolimSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'masul_shaxs', 'tel', 'manzil']


class BolimgaDoriViewSet(ModelViewSet):
    queryset = BolimgaDori.objects.all()
    serializer_class = serializers.BolimgaDoriSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BolimgaDoriFilter


class HodimViewSet(ModelViewSet):
    queryset = Hodim.objects.all()
    serializer_class = serializers.HodimSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'middle_name', 'lavozimi']


class HisoblanganOylikViewSet(ModelViewSet):
    queryset = HisoblanganOylik.objects.all()
    serializer_class = serializers.HisoblanganOylikSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HisoblanganOylikFilter


class OlinganOylikViewSet(ModelViewSet):
    queryset = OlinganOylik.objects.all()
    serializer_class = serializers.OlinganOylikSerializer
    permission_classes = [IsAuthenticated]

    
class HarajatViewSet(ModelViewSet):
    queryset = Harajat.objects.all().order_by('-date')
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


class KirimDorilarViewSet(ModelViewSet):
    queryset = KirimDorilar.objects.all().order_by('-date')
    serializer_class = serializers.KirimDorilarSerializer
    permission_classes = [IsAuthenticated]


class HozirgiSana(APIView):
    def get(self, request):
        today = datetime.today()
        d = {
            "sana": str(today)[:10],
            "soat": str(today)[11:13],
            "daqiqa": str(today)[14:16]
        }
        return Response(d)