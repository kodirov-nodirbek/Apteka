from datetime import datetime

from rest_framework import serializers
from .models import (Apteka, Firma, FirmaSavdolari, Nasiyachi, Nasiya, KunlikSavdo, Bolim, HisoblanganOylik, Harajat)

class AptekaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apteka
        fields = ['id', 'name', 'address', 'jami_qoldiq', 'last_update']

class FirmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firma
        fields = ['id', 'name', 'masul_shaxs', 'phone', 'jami_haqi', 'eng_yaqin_tolov_muddati']

class FirmaSavdolariSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirmaSavdolari
        fields = ['id', 'apteka_id', 'firma_id', 'shartnoma_raqami', 'harid_sanasi', 'tolov_muddati', 'tolangan_summalar', 'tolandi', 'tan_narxi', 'sotish_narxi', 'jami_tolangan_summa', 'jami_qarz']

    def add_payment(self, instance, validated_data):
        paid_amount = validated_data.get('paid_amount')
        payment_date = datetime.now()  # You can replace this with the actual payment date
        instance.add_payment(paid_amount, payment_date)

class NasiyachiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nasiyachi
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'phone', 'address', 'passport', 'created_at', 'jami_qarzi']


class NasiyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nasiya
        fields = ['id', 'chek_raqami', 'date', 'time', 'nasiya_summasi', 'tolangan_summa', 'tolov_tarixi', 'tolov_muddati', 'tolandi', 'nasiyachi_id']
        
class KunlikSavdoSerializer(serializers.ModelSerializer):
    class Meta:
        model = KunlikSavdo
        fields = ['id', 'date', 'jami_summa']

class BolimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bolim
        fields = ['id', 'bolim_nomi']
        
class HisoblanganOylikSerializer(serializers.ModelSerializer):
    class Meta:
        model = HisoblanganOylik
        fields = ['id', 'hodim', 'oylik_tarixi', 'oylik']

class HarajatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harajat
        fields = ['id', 'date', 'harajat_summasi']