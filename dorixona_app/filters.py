import django_filters
from .models import TopshirilganPul, KunlikSavdo, FirmaSavdolari, Nasiyachi, Nasiya, Harajat, TovarYuborishFilial


class FirmaSavdolariFilter(django_filters.FilterSet):
    apteka_id = django_filters.NumberFilter(field_name='apteka_id', lookup_expr='exact')
    firma_id = django_filters.NumberFilter(field_name='firma_id', lookup_expr='exact')
    shartnoma_raqami = django_filters.NumberFilter(field_name='shartnoma_raqami', lookup_expr='exact')
    date = django_filters.DateFilter(field_name='date', lookup_expr='date')
    from_date = django_filters.DateFilter(field_name='date', lookup_expr='date__gte')
    to_date = django_filters.DateFilter(field_name='date', lookup_expr='date__lte')

    class Meta:
        model = FirmaSavdolari
        fields = []


class NasiyachiFilter(django_filters.FilterSet):
    apteka_id = django_filters.NumberFilter(field_name='apteka_id', lookup_expr='exact')
    
    class Meta:
        model = Nasiyachi
        fields = []


class NasiyaFilter(django_filters.FilterSet):
    apteka_id = django_filters.NumberFilter(field_name='apteka_id', lookup_expr='exact')
    chek_raqami = django_filters.NumberFilter(field_name='chek_raqami', lookup_expr='exact')
    
    class Meta:
        model = Nasiya
        fields = []


class KunlikSavdoFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', lookup_expr='date')
    apteka_id = django_filters.NumberFilter(field_name='apteka_id', lookup_expr='exact')
    from_date = django_filters.DateFilter(field_name='date', lookup_expr='date__gte')
    to_date = django_filters.DateFilter(field_name='date', lookup_expr='date__lte')

    class Meta:
        model = KunlikSavdo
        fields = []


class TopshirilganPulFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', lookup_expr='date')
    apteka_id = django_filters.NumberFilter(field_name='apteka_id', lookup_expr='exact')
    qabul_qilindi = django_filters.BooleanFilter(field_name='qabul_qilindi', lookup_expr='exact')
    from_date = django_filters.DateFilter(field_name='date', lookup_expr='date__gte')
    to_date = django_filters.DateFilter(field_name='date', lookup_expr='date__lte')

    class Meta:
        model = TopshirilganPul
        fields = []


class HarajatFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', lookup_expr='date')
    apteka_id = django_filters.NumberFilter(field_name='apteka_id', lookup_expr='exact')
    hodim_id = django_filters.NumberFilter(field_name='hodim_id', lookup_expr='exact')
    from_date = django_filters.DateFilter(field_name='date', lookup_expr='date__gte')
    to_date = django_filters.DateFilter(field_name='date', lookup_expr='date__lte')

    class Meta:
        model = Harajat
        fields = []


class HarajatFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', lookup_expr='date')
    apteka_id = django_filters.NumberFilter(field_name='apteka_id', lookup_expr='exact')
    hodim_id = django_filters.NumberFilter(field_name='hodim_id', lookup_expr='exact')
    from_date = django_filters.DateFilter(field_name='date', lookup_expr='date__gte')
    to_date = django_filters.DateFilter(field_name='date', lookup_expr='date__lte')

    class Meta:
        model = Harajat
        fields = []


class TovarYuborishFilialFilter(django_filters.FilterSet):
    sent_time = django_filters.DateFilter(field_name='sent_time', lookup_expr='date')
    from_filial = django_filters.NumberFilter(field_name='from_filial', lookup_expr='exact')
    to_filial = django_filters.NumberFilter(field_name='to_filial', lookup_expr='exact')
    accepted = django_filters.BooleanFilter(field_name='accepted', lookup_expr='exact')

    class Meta:
        model = TovarYuborishFilial
        fields = []