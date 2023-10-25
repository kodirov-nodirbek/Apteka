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
router.register("hisoblanganoyliklar", views.HisoblanganOylikViewSet)
router.register("harajatlar", views.HarajatViewSet)
router.register("hodimlar", views.HodimViewSet)
router.register("tovaryuborishfilial", views.TovarYuborishFilialViewSet)



urlpatterns = [
    path('sana/', views.HozirgiSana.as_view(), name='sana'),
] + router.urls