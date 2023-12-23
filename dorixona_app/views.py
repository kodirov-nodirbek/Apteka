from datetime import datetime
from rest_framework import filters, status, generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .filters import (KunlikSavdoFilter, FirmaSavdolariFilter, NasiyachiFilter, NasiyaFilter, HarajatFilter, TovarYuborishFilialFilter, BolimgaDoriFilter, HisoblanganOylikFilter, OlinganOylikFilter, KirimDorilarFilter)
from . import serializers
from .models import (Apteka, Firma, FirmaSavdolari, Nasiyachi, Nasiya, KunlikSavdo, Bolim, BolimgaDori, Hodim, HisoblanganOylik, Harajat, TovarYuborishFilial, KirimDorilar, OlinganOylik)


class AptekaViewSet(ModelViewSet):
    serializer_class = serializers.AptekaSerializer
    permission_classes = [IsAuthenticated]
    queryset = Apteka.objects.all()


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
        izoh = data.get("izoh", "-")

        tolov = naqd+plastik
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
            Harajat.objects.create(apteka_id=Apteka.objects.get(id=apteka_id), naqd_pul=naqd, plastik=plastik, firma_uchun=True, firma_id=firma_object, izoh=izoh)
        serializer = serializers.FirmaSerializer(firma_object)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class FirmaSavdolariViewSet(ModelViewSet):
    queryset = FirmaSavdolari.objects.all()
    serializer_class = serializers.FirmaSavdolariSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FirmaSavdolariFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        jami_tolandi = sum(summa.jami_tolangan_summa() for summa in queryset)
        jami_qarz = sum(summa.jami_qarz() for summa in queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"jami_tolangan_summalar": jami_tolandi, "jami_qarzlar": jami_qarz, "data": serializer.data})


class NasiyachiViewSet(ModelViewSet):
    queryset = Nasiyachi.objects.all()
    serializer_class = serializers.NasiyachiSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = NasiyachiFilter
    search_fields = ['first_name', 'last_name', 'passport', 'phone']
    

class NasiyaViewSet(ModelViewSet):
    queryset = Nasiya.objects.all().order_by('tolov_muddati')
    serializer_class = serializers.NasiyaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NasiyaFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['chek_raqami', 'date']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        jami_tolandi = sum(summa.jami_tolangan_summa() for summa in queryset)
        jami_qarz = sum(summa.qolgan_qarz() for summa in queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"jami_tolangan_summalar": jami_tolandi, "qolgan_qarz": jami_qarz, "data": serializer.data})

    
class KunlikSavdoViewSet(ModelViewSet):
    queryset = KunlikSavdo.objects.all().order_by('-date')
    serializer_class = serializers.KunlikSavdoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = KunlikSavdoFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        jami_naqd = sum(naqd.naqd_pul for naqd in queryset)
        jami_terminal = sum(terminal.terminal for terminal in queryset)
        jami_plastik = sum(plastik.card_to_card for plastik in queryset)
        jami_inkassa = sum(inkassa.inkassa for inkassa in queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"jami_naqd": jami_naqd, "jami_terminal": jami_terminal, "jami_card_to_card": jami_plastik, "jami_inkassa": jami_inkassa, "data": serializer.data})
    

class KunlikSavdoUpdateView(generics.UpdateAPIView):
    queryset = KunlikSavdo.objects.all()
    serializer_class = serializers.KunlikSavdoSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        
        id_list = request.data.get('id_list', [])
        
        instances = self.get_queryset().filter(id__in=id_list)
        
        for instance in instances:
            instance.accepted = True
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        jami = sum(oylik.hisoblangan_oylik() for oylik in queryset)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"jami_oylik": jami, "data": serializer.data})


class OlinganOylikViewSet(ModelViewSet):
    queryset = OlinganOylik.objects.all()
    serializer_class = serializers.OlinganOylikSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OlinganOylikFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        jami = sum(oylik.summa() for oylik in queryset)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"jami_olingan": jami, "data": serializer.data})
    
    
class HarajatViewSet(ModelViewSet):
    queryset = Harajat.objects.all().order_by('-date')
    serializer_class = serializers.HarajatSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HarajatFilter
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        jami = sum(harajat.jami_harajat() for harajat in queryset)
        jami_plastik = sum(harajat.plastik for harajat in queryset)
        jami_naqd = sum(harajat.naqd_pul for harajat in queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'jami_naqd': jami_naqd, 'jami_plastik': jami_plastik, 'jami_harajatlar': jami, 'data': serializer.data})


class TovarYuborishFilialViewSet(ModelViewSet):
    queryset = TovarYuborishFilial.objects.all()
    serializer_class = serializers.TovarYuborishFilialSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TovarYuborishFilialFilter
    
    def get_name(self):
        return self.name
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        jami = sum(tovar.tovar_summasi for tovar in queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'jami_tovarlar_summasi': jami, 'data': serializer.data})


class KirimDorilarViewSet(ModelViewSet):
    queryset = KirimDorilar.objects.all().order_by('-date')
    serializer_class = serializers.KirimDorilarSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = KirimDorilarFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        jami = sum(kirim.kirim_summasi for kirim in queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'jami_kirim_summasi': jami, 'data': serializer.data})
    

class HozirgiSana(APIView):
    def get(self, request):
        today = datetime.today()
        d = {
            "sana": str(today)[:10],
            "soat": str(today)[11:13],
            "daqiqa": str(today)[14:16]
        }
        return Response(d)