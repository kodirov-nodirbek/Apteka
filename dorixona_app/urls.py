from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register("aptekalar", views.AptekaViewSet)
router.register(r'firmalar', views.FirmaViewSet, basename='firmalar')
router.register(r'firma_savdolari', views.FirmaSavdolariViewSet, basename='firmasavdolari')
router.register("nasiyachilar", views.NasiyachiViewSet)
router.register("nasiyalar", views.NasiyaViewSet)
router.register("kunliksavdo", views.KunlikSavdoViewSet)
router.register("bolimlar", views.BolimViewSet)
router.register("bolimgadorilar", views.BolimgaDoriViewSet)
router.register("hisoblanganoyliklar", views.HisoblanganOylikViewSet)
router.register("oliganoyliklar", views.OlinganOylikViewSet)
router.register("harajatlar", views.HarajatViewSet)
router.register("hodimlar", views.HodimViewSet)
router.register(r"tovaryuborishfilial", views.TovarYuborishFilialViewSet, basename="tovaryuborishfilial")
router.register(r"kirimdorilar", views.KirimDorilarViewSet, basename="kirimdorilar")


urlpatterns = [
    path('sana/', views.HozirgiSana.as_view(), name='sana'),
    path('kunliksavdo/qabul_qildi/', views.KunlikSavdoUpdateView.as_view(), name='update_qabul_qildi'),
] + router.urls