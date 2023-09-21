from decimal import Decimal
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Apteka(models.Model):
    class Meta:
        verbose_name = "Apteka"
        verbose_name_plural = "Aptekalar"
    name = models.CharField(max_length=155)
    address = models.CharField(max_length=255)
    jami_qoldiq = models.DecimalField(max_digits=14, decimal_places=2)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Firma(models.Model):
    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmalar"
    name = models.CharField(max_length=155)
    masul_shaxs = models.CharField(max_length=255)
    phone = models.CharField(max_length=22)
    # eng_yaqin_tolov_sanasi = models.DateField()
    
    def __str__(self):
        return self.name

    def jami_haqi(self):
        firma_savdolari = FirmaSavdolari.objects.filter(firma_id=self)
        total_tan_narxi = sum(savdo.tan_narxi for savdo in firma_savdolari)
        
        total_tolangan_summa = sum(
            savdo.jami_tolangan_summa() if savdo.tolangan_summalar else 0
            for savdo in firma_savdolari
        )
        
        return total_tan_narxi - total_tolangan_summa
    
    def eng_yaqin_tolov_muddati(self):
        firma_savdolari = FirmaSavdolari.objects.filter(firma_id=self).order_by('tolov_muddati')
        return firma_savdolari.first().tolov_muddati if firma_savdolari else 0

class FirmaSavdolari(models.Model):
    class Meta:
        verbose_name = "Firma savdosi"
        verbose_name_plural = "Firma savdolari"
    
    apteka_id = models.ForeignKey(to=Apteka, on_delete=models.CASCADE)
    firma_id = models.ForeignKey(to=Firma, on_delete=models.CASCADE)
    shartnoma_raqami = models.CharField(max_length=50)
    harid_sanasi = models.DateTimeField(auto_now=True)
    tolov_muddati = models.DateField()
    tolangan_summalar = models.JSONField(default=list, null=True)
    tolandi = models.BooleanField(default=False)
    tan_narxi = models.DecimalField(max_digits=14, decimal_places=2)
    sotish_narxi = models.DecimalField(max_digits=14, decimal_places=2)

    def jami_tolangan_summa(self):
        tolangan_summalar = self.tolangan_summalar or []
        return sum(item.get('summa', 0) for item in tolangan_summalar)
    def jami_qarz(self):
        tan_narxi = self.tan_narxi or Decimal(0)
        tolangan_summa = self.jami_tolangan_summa()
        return tan_narxi - tolangan_summa

    def add_payment(self, paid_amount, payment_date):
        if self.tolangan_summalar is None:
            self.tolangan_summalar = []

        payment_data = {
            'summa': paid_amount,
            'harid_sanasi': payment_date.isoformat() if payment_date else timezone.now().isoformat()
        }
        if payment_data['summa'] != None:
            self.tolangan_summalar.append(payment_data)
            self.save()

class Nasiyachi(models.Model):
    class Meta:
        verbose_name = "Nasiyachi"
        verbose_name_plural = "Nasiyachilar"
    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    middle_name = models.CharField(max_length=155)
    phone = models.CharField(max_length=155)
    address = models.CharField(max_length=155)
    passport = models.CharField(max_length=22, null=True)
    created_at = models.DateField(auto_now=True)


    def jami_qarzi(self):
        return sum(nasiya.qolgan_qarz() for nasiya in self.nasiya_set.filter(tolandi=False))

    
class Nasiya(models.Model):
    class Meta:
        verbose_name = "Nasiya"
        verbose_name_plural = "Nasiyalar"
    chek_raqami = models.PositiveBigIntegerField()
    nasiya_summasi = models.DecimalField(max_digits=14, decimal_places=2)
    tolangan_summa = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    tolov_tarixi = models.JSONField(default=dict)
    tolandi = models.BooleanField(default=False)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    tolov_muddati = models.DateField()
    nasiyachi_id = models.ForeignKey(to=Nasiyachi, on_delete=models.CASCADE)

    def qolgan_qarz(self):
        return self.nasiya_summasi-self.tolangan_summa


class KunlikSavdo(models.Model):
    class Meta:
        verbose_name = "Kunliksavdo"
        verbose_name_plural = "Kunliksavdolar"
    jami_summa = models.DecimalField(max_digits=14, decimal_places=2)
    date = models.DateField()


class Bolim(models.Model):
    class Meta:
        verbose_name = "Bolim"
        verbose_name_plural = "Bolimlar"
    bolim_nomi = models.CharField(max_length=255)


class HisoblanganOylik(models.Model):
    class Meta:
        verbose_name = "Hisoblanganoylik"
        verbose_name_plural = "Hisoblanganoyliklar"
    oylik = models.DecimalField(max_digits=14, decimal_places=2)
    hodim = models.ForeignKey(to=User, on_delete=models.PROTECT)
    oylik_tarixi = models.JSONField(default=dict) 


class Harajat(models.Model):
    class Meta:
        verbose_name = "Harajat"
        verbose_name_plural = "Harajatlar"

    harajat_summasi = models.DecimalField(max_digits=14, decimal_places=2)
    date = models.DateField(auto_now=True)
