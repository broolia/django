from django_filters import rest_framework as filters

from advertisements.models import Advertisement,AdvertisementStatusChoices
    


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = filters.DateFromToRangeFilter()

    # Фильтр по статусу (использует choices из модели)
    status = filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)

    # Фильтр по создателю (по ID пользователя)
    creator = filters.NumberFilter(field_name='creator_id')


    

    class Meta:
        model = Advertisement
        fields = ['created_at', 'status', 'creator']
