from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from advertisements.models import Advertisement 
from advertisements.serializers import AdvertisementSerializer
from advertisements.permissions import IsOwnerOrReadOnly 
from advertisements.filters import AdvertisementFilter


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    # Основной queryset для всех объявлений
    queryset = Advertisement.objects.all()
    
    serializer_class = AdvertisementSerializer
    
    filter_backends = [DjangoFilterBackend]
    
    filterset_class = AdvertisementFilter
    

   

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == 'create':
            return [IsAuthenticated()]
        
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]    
        return [AllowAny()]
