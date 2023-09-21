from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("aptekalar", views.AptekaViewSet)
router.register("firmalar", views.FirmaViewSet)
# router.register("firma_savdolari", views.FirmaSavdolariViewSet)
router.register(r'firma_savdolari', views.FirmaSavdolariViewSet, basename='firmasavdolari')
router.register("nasiyachilar", views.NasiyachiViewSet)
router.register("nasiyalar", views.NasiyaViewSet)
router.register("kunliksavdo", views.KunlikSavdoViewSet)
router.register("bolimlar", views.BolimViewSet)
router.register("hisoblanganoyliklar", views.HisoblanganOylikViewSet)
router.register("harajatlar", views.HarajatViewSet)



urlpatterns = [
    path('sana/', views.HozirgiSana.as_view(), name='sana'),
] + router.urls