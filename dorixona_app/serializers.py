from datetime import datetime

from rest_framework import serializers
from .models import (Apteka, Firma, FirmaSavdolari, Nasiyachi, Nasiya, KunlikSavdo, Bolim, Hodim, HisoblanganOylik, Harajat, TovarYuborishFilial)


class AptekaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apteka
        fields = ['id', 'name', 'address', 'jami_qoldiq', 'last_update']


class FirmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firma
        fields = ['id', 'name', 'masul_shaxs', 'phone', 'jami_haqi', 'haqdor', 'eng_yaqin_tolov_muddati']


class FirmaSavdolariSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirmaSavdolari
        fields = ['id', 'apteka_id', 'firma_id', 'shartnoma_raqami', 'qaytarilgan_tovar_summasi', 'harid_sanasi', 'tolov_muddati', 'tolangan_summalar', 'tolandi', 'tan_narxi', 'sotish_narxi', 'jami_tolangan_summa', 'jami_qarz', 'ochirishga_sorov']

    def add_payment(self, instance, validated_data):
        paid_amount = validated_data.get('paid_amount')
        payment_date = datetime.now()
        instance.add_payment(paid_amount, payment_date)

class FirmaTolovPatch(serializers.Serializer):
    qaytarilgan_tovar_summasi = serializers.DecimalField(max_digits=14, decimal_places=0)
    tolangan_summalar = serializers.JSONField()


class NasiyachiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nasiyachi
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'phone', 'address', 'passport', 'created_at', 'jami_qarzi', 'apteka_id']


class NasiyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nasiya
        fields = ['id', 'chek_raqami', 'date', 'time', 'nasiya_summasi', 'tolangan_summalar', 'jami_tolangan_summa', 'tolov_muddati', 'tolandi', 'nasiyachi_id', 'apteka_id']
    
    tolandi = serializers.SerializerMethodField()

    def get_tolandi(self, obj):
        return obj.qolgan_qarz() <= 0


class KunlikSavdoSerializer(serializers.ModelSerializer):
    class Meta:
        model = KunlikSavdo
        fields = ['id', 'naqd_pul', 'terminal', 'card_to_card', 'inkassa', 'jami_summa', 'date']


class BolimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bolim
        fields = ['id', 'bolim_nomi']


class HodimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hodim
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'apteka_id']
        

class HisoblanganOylikSerializer(serializers.ModelSerializer):
    class Meta:
        model = HisoblanganOylik
        fields = ['id', 'hodim', 'oylik_tarixi', 'oylik']


class HarajatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harajat
        fields = ['id', 'naqd_pul', 'plastik', 'izoh', 'hodim_id', 'apteka_id', 'jami_harajat']


class TovarYuborishFilialSerializer(serializers.ModelSerializer):
    to_filial = AptekaSerializer()

    def filial(self):
        qs = Apteka.objects.filter(id=self.to_filial)
        serializer = AptekaSerializer(instance=qs, many=True)
        return serializer.data
    
    class Meta:
        model = TovarYuborishFilial
        fields = ['id', 'tovar_summasi', "from_filial", "to_filial", "accepted"]
