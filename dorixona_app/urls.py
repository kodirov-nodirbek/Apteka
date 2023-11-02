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
router.register("topshirilganpullar", views.TopshirilganPulViewSet)
router.register("bolimlar", views.BolimViewSet)
router.register("bolimgadorilar", views.BolimgaDoriViewSet)
router.register("hisoblanganoyliklar", views.HisoblanganOylikViewSet)
router.register("harajatlar", views.HarajatViewSet)
router.register("hodimlar", views.HodimViewSet)
router.register(r"tovaryuborishfilial", views.TovarYuborishFilialViewSet, basename="tovaryuborishfilial")


urlpatterns = [
    path('sana/', views.HozirgiSana.as_view(), name='sana'),
    # path('aptekastatistics/<int:apteka_id>', views.AptekaStatisticsView.as_view(), name='aptekastatistics'),
] + router.urls