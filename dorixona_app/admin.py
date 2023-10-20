from django.contrib import admin
from .models import (Apteka, Firma, FirmaSavdolari, Nasiyachi, Nasiya, KunlikSavdo, Bolim, HisoblanganOylik, Harajat)

@admin.register(Apteka)
class AptekaAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "jami_qoldiq")
    search_fields = ("name",)


@admin.register(Firma)
class FirmaAdmin(admin.ModelAdmin):
    list_display = ("name", "eng_yaqin_tolov_muddati")
    search_fields = ("name",)

@admin.register(FirmaSavdolari)
class FimaSavdolariAdmin(admin.ModelAdmin):
    list_display = ('id', "firma_id", "harid_sanasi", "tan_narxi")
    search_fields = ("harid_sanasi",)
    list_display_links = ("firma_id",)
    sortable_by = ('tolov_muddati')

@admin.register(Nasiyachi)
class NasiyachiAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone")
    search_fields = ("first_name",)


@admin.register(Nasiya)
class NasiyaAdmin(admin.ModelAdmin):
    list_display = ("date", "nasiya_summasi")
    search_fields = ("date", )


@admin.register(KunlikSavdo)
class KunlikSavdoAdmin(admin.ModelAdmin):
    list_display = ("date", "jami_summa")
    search_fields = ("date",)


@admin.register(Bolim)
class BolimAdmin(admin.ModelAdmin):
    list_display = ("bolim_nomi", )
    search_fields = ("bolim_nomi", )


@admin.register(HisoblanganOylik)
class HisoblanganOylikAdmin(admin.ModelAdmin):
    list_display = ("hodim", "oylik")
    search_fields = ("hodim", )


@admin.register(Harajat)
class HarajatAdmin(admin.ModelAdmin):
    list_display = ("date", "harajat_summasi")
    search_fields = ("date", )