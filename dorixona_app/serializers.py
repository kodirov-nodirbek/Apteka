from datetime import datetime

from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from .models import (Apteka, Firma, FirmaSavdolari, Nasiyachi, Nasiya, KunlikSavdo, TopshirilganPul, Bolim, BolimgaDori, Hodim, HisoblanganOylik, Harajat, TovarYuborishFilial)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'id': self.user.id})
        data.update({'role': self.user.role})
        data.update({"token": data.pop('access')})
        # and everything else you want to send in the response
        return data
    
    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)
        return token


class AptekaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apteka
        fields = ['id', 'name', 'role', 'address', 'jami_qoldiq', 'last_update']


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

    # def to_representation(self, instance):
    #     data = super(FirmaSavdolariSerializer, self).to_representation(instance)
    #     firma_savdolari = FirmaSavdolari.objects.filter(apteka_id=self.request.user)
    #     data.update({"firma_savdolari": firma_savdolari})
    #     return data


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
        fields = ['id', 'chek_raqami', 'date', 'nasiya_summasi', 'tolangan_summalar', 'jami_tolangan_summa', 'tolov_muddati', 'tolandi', 'nasiyachi_id', 'apteka_id']
    
    tolandi = serializers.SerializerMethodField()

    def get_tolandi(self, obj):
        return obj.qolgan_qarz() <= 0


class KunlikSavdoSerializer(serializers.ModelSerializer):
    class Meta:
        model = KunlikSavdo
        fields = ['id', 'apteka_id', 'naqd_pul', 'terminal', 'card_to_card', 'inkassa', 'jami_summa', 'date']


class TopshirilganPulSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopshirilganPul
        fields = "__all__"


class BolimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bolim
        fields = "__all__"


class BolimgaDoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = BolimgaDori
        fields = "__all__"


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
        fields = ['id', 'naqd_pul', 'plastik', 'izoh', 'hodim_id', 'apteka_id', 'jami_harajat', 'date']


class TovarYuborishFilialSerializer(serializers.ModelSerializer):
    class Meta:
        model = TovarYuborishFilial
        fields = ['id', 'tovar_summasi', 'from_filial', 'apteka', 'to_filial', 'accepted', 'sent_time', 'accepted_time']
