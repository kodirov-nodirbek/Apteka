from rest_framework import serializers
from .models import (Apteka, Firma, FirmaSavdolari, Nasiyachi, Nasiya, KunlikSavdo, Bolim, BolimgaDori, Hodim, HisoblanganOylik, Harajat, TovarYuborishFilial, KirimDorilar, OlinganOylik)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data.update({'id': self.user.id})
        data.update({'role': self.user.role})
        data.update({"token": data.pop('access')})
        return data
    
    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)
        return token


class AptekaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apteka
        fields = ['id', 'name', 'role', 'address', 'jami_qoldiq', 'last_update', 'get_nasiyalar', 'topshiriladigan_pul']


class FirmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firma
        fields = ['id', 'name', 'masul_shaxs', 'phone', 'jami_haqi', 'haqdor', 'eng_yaqin_tolov_muddati']


class FirmaSavdolariSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirmaSavdolari
        fields = ['id', 'firma_id', 'shartnoma_raqami', 'qaytarilgan_tovar_summasi', 'harid_sanasi', 'tolov_muddati', 'tolangan_summalar', 'tolandi', 'tan_narxi', 'sotish_narxi', 'jami_tolangan_summa', 'jami_qarz']


class NasiyachiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nasiyachi
        fields = ['id', 'apteka_id', 'first_name', 'last_name', 'middle_name', 'phone', 'address', 'passport', 'created_at', 'jami_qarzi']


class NasiyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nasiya
        fields = ['id', 'chek_raqami', 'date', 'nasiya_summasi', 'tolangan_summalar', 'jami_tolangan_summa', 'tolov_muddati', 'nasiyachi_id', 'apteka_id', 'qolgan_qarz', 'tolandi']


class KunlikSavdoSerializer(serializers.ModelSerializer):
    class Meta:
        model = KunlikSavdo
        fields = ['id', 'apteka_id', 'apteka_name', 'naqd_pul', 'terminal', 'card_to_card', 'inkassa', 'jami_summa', 'date', 'topshirishga_pul', 'accepted']


class BolimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bolim
        fields = "__all__"


class BolimgaDoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = BolimgaDori
        fields = ['id', 'summa', 'apteka_id', 'apteka_name', 'bolim_id', 'date', 'bolim_name', 'accepted']


class HodimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hodim
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'apteka_id', 'apteka_name', 'active', 'created_at', 'ish_haqi_kunlik', 'lavozimi']
        

class HisoblanganOylikSerializer(serializers.ModelSerializer):
    class Meta:
        model = HisoblanganOylik
        fields = ['id', 'hodim_id', 'hisoblangan_oylik', 'qolga_tegishi', 'ishlagan_kunlar', 'date']


class OlinganOylikSerializer(serializers.ModelSerializer):
    class Meta:
        model = OlinganOylik
        fields = ['id', 'hodim_id', 'hodim_name', 'apteka_id', "apteka_nomi", 'naqd_pul', 'card_to_card', 'summa', 'date']


class HarajatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harajat
        fields = ['id', 'naqd_pul', 'plastik', 'izoh', 'apteka_id', "apteka_nomi", 'jami_harajat', 'date', 'firma_uchun', 'firma_id', 'firma_nomi']


class TovarYuborishFilialSerializer(serializers.ModelSerializer):
    class Meta:
        model = TovarYuborishFilial
        fields = ['id', 'tovar_summasi', 'from_filial', 'to_filial', 'from_apteka_name', 'to_apteka_name', 'accepted', 'sent_time', 'accepted_time']


class KirimDorilarSerializer(serializers.ModelSerializer):
    class Meta:
        model = KirimDorilar
        fields = "__all__"