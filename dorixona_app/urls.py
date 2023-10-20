from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("aptekalar", views.AptekaViewSet)
# router.register("firmalar", views.FirmaViewSet)
router.register(r'firmalar', views.FirmaViewSet, basename='firmalar') 
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
    # path('firmalar/<int:pk>/', views.FirmaViewSet.as_view({'patch': 'partial_update', 'get':'list'})),
] + router.urls