from decimal import Decimal
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class Apteka(AbstractUser):
    class Meta:
        verbose_name = "Apteka"
        verbose_name_plural = "Aptekalar"
    role = models.CharField(max_length=55)
    name = models.CharField(max_length=155)
    address = models.CharField(max_length=255)
    jami_qoldiq = models.DecimalField(max_digits=14, decimal_places=0, default=Decimal(0))
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_nasiyalar(self):
        nasiyalar = Nasiya.objects.filter(apteka_id=self)
        summa = 0
        for nasiya in nasiyalar:
            summa+=nasiya.qolgan_qarz()
        return summa
    
    def topshiriladigan_pul(self):
        summalar = KunlikSavdo.objects.filter(apteka_id__id=self.id).filter(accepted=False)
        pullar = 0
        for summa in summalar:
            pullar+=summa.topshirishga_pul()
        return pullar


class Firma(models.Model):
    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmalar"
    name = models.CharField(max_length=155)
    masul_shaxs = models.CharField(max_length=255)
    phone = models.CharField(max_length=22)
    
    def __str__(self):
        return self.name

    def jami_haqi(self):
        firma_savdolari = FirmaSavdolari.objects.filter(firma_id=self)
        total_tan_narxi = sum(savdo.tan_narxi for savdo in firma_savdolari)
        
        total_tolangan_summa = sum(
            savdo.jami_tolangan_summa() if savdo.tolangan_summalar else 0
            for savdo in firma_savdolari
        )
        qaytarilgan_summa = sum(
            savdo.qaytarilgan_tovar_summasi for savdo in firma_savdolari
        )
        return total_tan_narxi - total_tolangan_summa - qaytarilgan_summa
    
    def haqdor(self):
        return int(self.jami_haqi())>0

    def eng_yaqin_tolov_muddati(self):
        firma_savdolari = FirmaSavdolari.objects.filter(firma_id=self).order_by('tolov_muddati')
        return firma_savdolari.first().tolov_muddati if firma_savdolari else 0


class FirmaSavdolari(models.Model):
    class Meta:
        verbose_name = "Firma savdosi"
        verbose_name_plural = "Firma savdolari"

    firma_id = models.ForeignKey(to=Firma, on_delete=models.CASCADE)
    shartnoma_raqami = models.CharField(max_length=50)
    harid_sanasi = models.DateTimeField(auto_now_add=True)
    tolov_muddati = models.DateField()
    tolangan_summalar = models.JSONField(default=list)
    tan_narxi = models.DecimalField(max_digits=14, decimal_places=0)
    sotish_narxi = models.DecimalField(max_digits=14, decimal_places=0)
    qaytarilgan_tovar_summasi = models.DecimalField(max_digits=14, decimal_places=0, default=Decimal(0))
    izoh = models.TextField(null=True, blank=True)
    tolandi = models.BooleanField(default=False)

    def jami_tolangan_summa(self):
        tolangan_summalar = self.tolangan_summalar or []
        return sum(int(item.get('summa', 0)) for item in tolangan_summalar)
    
    def jami_qarz(self):
        tan_narxi = self.tan_narxi or Decimal(0)
        tolangan_summa = self.jami_tolangan_summa()
        qaytarilgan_tovar_summasi = self.qaytarilgan_tovar_summasi or Decimal(0)
        return tan_narxi - tolangan_summa - qaytarilgan_tovar_summasi


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
    created_at = models.DateTimeField(auto_now_add=True)
    apteka_id = models.ForeignKey(to=Apteka, on_delete=models.CASCADE)

    def jami_qarzi(self):
        return sum(nasiya.qolgan_qarz() for nasiya in self.nasiya_set.filter())

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Nasiya(models.Model):
    class Meta:
        verbose_name = "Nasiya"
        verbose_name_plural = "Nasiyalar"
    chek_raqami = models.CharField(max_length=55, null=True)
    nasiya_summasi = models.DecimalField(max_digits=14, decimal_places=0)
    tolangan_summalar = models.JSONField(default=list)
    date = models.DateTimeField(auto_now_add=True)
    tolov_muddati = models.DateField()
    nasiyachi_id = models.ForeignKey(to=Nasiyachi, on_delete=models.CASCADE)
    apteka_id = models.ForeignKey(to=Apteka, on_delete=models.CASCADE)
    tolandi = models.BooleanField(default=False)

    def jami_tolangan_summa(self):
        tolangan_summalar = self.tolangan_summalar or []
        return sum(int(item.get('summa', 0)) for item in tolangan_summalar)

    def qolgan_qarz(self):
        return self.nasiya_summasi-self.jami_tolangan_summa()
  
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.qolgan_qarz() <= 0:
            self.tolandi = True

        super().save(force_insert, force_update, using, update_fields)


class KunlikSavdo(models.Model):
    class Meta:
        verbose_name = "Kunlik savdo"
        verbose_name_plural = "Kunlik savdolar"
    card_to_card = models.DecimalField(max_digits=14, decimal_places=0)
    terminal = models.DecimalField(max_digits=14, decimal_places=0)
    naqd_pul = models.DecimalField(max_digits=14, decimal_places=0)
    inkassa = models.DecimalField(max_digits=14, decimal_places=0)
    apteka_id = models.ForeignKey(to=Apteka, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())
    accepted = models.BooleanField(default=False)

    def apteka_name(self):
        return self.apteka_id.name

    def jami_summa(self):
        return self.naqd_pul+self.terminal+self.card_to_card+self.inkassa

    def topshirishga_pul(self):
        date = self.date.date()
        harajatlar = Harajat.objects.filter(apteka_id=self.apteka_id).filter(date__date=date)
        rosxod = 0
        for harajat in harajatlar:
            rosxod += harajat.naqd_pul+harajat.plastik
        topshirishga = self.naqd_pul+self.card_to_card-rosxod
        return topshirishga

    def decrease(self):
        return self.terminal+self.inkassa
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.accepted:
            apteka = Apteka.objects.get(id=self.apteka_id.id)
            apteka.jami_qoldiq-=Decimal(self.decrease())
            apteka.save()
        return super().save(force_insert, force_update, using, update_fields)


class Bolim(models.Model):
    class Meta:
        verbose_name = "Bolim"
        verbose_name_plural = "Bolimlar"
    name = models.CharField(max_length=255)
    masul_shaxs = models.CharField(max_length=155)
    tel = models.CharField(max_length=55)
    manzil = models.CharField(max_length=450)

    def __str__(self):
        return self.name


class BolimgaDori(models.Model):
    class Meta:
        verbose_name = "BolimgaDori"
        verbose_name_plural = "BolimgaDorilar"
    summa = models.DecimalField(max_digits=14, decimal_places=0)
    apteka_id = models.ForeignKey(Apteka, on_delete=models.CASCADE)
    bolim_id = models.ForeignKey(Bolim, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def bolim_name(self):
        return self.bolim_id.name

    def apteka_name(self):
        return self.apteka_id.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.accepted:
            apteka = Apteka.objects.get(id=self.apteka_id.id)
            apteka.jami_qoldiq-=self.summa
            apteka.save()
        return super().save(force_insert, force_update, using, update_fields)


class Hodim(models.Model):
    class Meta:
        verbose_name = "Hodim"
        verbose_name_plural = "Hodimlar"
    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    middle_name = models.CharField(max_length=155)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    apteka_id = models.ForeignKey(to=Apteka, on_delete=models.CASCADE)
    ish_haqi_kunlik = models.DecimalField(max_digits=14, decimal_places=0) #80000
    lavozimi = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def apteka_name(self):
        return self.apteka_id.name


class HisoblanganOylik(models.Model):
    class Meta:
        verbose_name = "Hisoblanganoylik"
        verbose_name_plural = "Hisoblanganoyliklar"
    ishlagan_kunlar = models.PositiveIntegerField()
    hodim_id = models.ForeignKey(to=Hodim, on_delete=models.PROTECT)
    date = models.DateTimeField()

    def hisoblangan_oylik(self):
        return self.hodim_id.ish_haqi_kunlik * self.ishlagan_kunlar

    def qolga_tegishi(self):
        olingan_oylik_sum = sum(oylik.summa() for oylik in OlinganOylik.objects.filter(hodim_id=self.hodim_id, date__month=self.date.month))
        jami = self.hisoblangan_oylik()
        return jami - olingan_oylik_sum


class OlinganOylik(models.Model):
    naqd_pul = models.DecimalField(max_digits=14, decimal_places=0, default=0)
    card_to_card = models.DecimalField(max_digits=14, decimal_places=0, default=0)
    date = models.DateTimeField(default=datetime.now())
    hodim_id = models.ForeignKey(Hodim, on_delete=models.CASCADE)
    apteka_id = models.ForeignKey(Apteka, on_delete=models.CASCADE)

    def apteka_nomi(self):
        return self.apteka_id.name

    def hodim_name(self):
        return f"{self.hodim_id.first_name} {self.hodim_id.last_name} {self.hodim_id.middle_name}"

    def summa(self):
        return self.naqd_pul+self.card_to_card


class Harajat(models.Model):
    class Meta:
        verbose_name = "Harajat"
        verbose_name_plural = "Harajatlar"
    naqd_pul = models.DecimalField(max_digits=14, decimal_places=0)
    plastik = models.DecimalField(max_digits=14, decimal_places=0)
    izoh = models.TextField()
    apteka_id = models.ForeignKey(to=Apteka, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    firma_uchun = models.BooleanField(default=False)
    firma_id = models.ForeignKey(Firma, on_delete=models.CASCADE, null=True)

    def apteka_nomi(self):
        return self.apteka_id.name

    def firma_nomi(self):
        return self.firma_id.name if self.firma_id else None

    def jami_harajat(self):
        return self.naqd_pul+self.plastik
  
    
class TovarYuborishFilial(models.Model):
    tovar_summasi = models.DecimalField(max_digits=14, decimal_places=0)
    from_filial = models.ForeignKey(Apteka, on_delete=models.CASCADE, related_name='outgoing_tovar_filials')
    to_filial = models.PositiveIntegerField()
    accepted = models.BooleanField(default=False)
    sent_time = models.DateTimeField(auto_now_add=True)
    accepted_time = models.DateTimeField(null=True)

    def from_apteka_name(self):
        return self.from_filial.name
    
    def to_apteka_name(self):
        return Apteka.objects.get(id=self.to_filial).name
        # return self.to_filial
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.accepted:
            to_filial = Apteka.objects.get(id=self.to_filial)
            from_filial = Apteka.objects.get(id=self.from_filial.id)
            from_filial.jami_qoldiq-=self.tovar_summasi
            to_filial.jami_qoldiq+=self.tovar_summasi
            from_filial.save()
            to_filial.save()
        return super(TovarYuborishFilial, self).save(force_insert=False, force_update=False, using=None, update_fields=None)


class KirimDorilar(models.Model):
    apteka_id = models.ForeignKey(Apteka, on_delete=models.CASCADE)
    kirim_summasi = models.DecimalField(max_digits=14, decimal_places=0)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        apteka = Apteka.objects.get(id=self.apteka_id.id)
        apteka.jami_qoldiq+=self.kirim_summasi
        apteka.save()
        return super().save(force_insert, force_update, using, update_fields)