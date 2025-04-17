from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, AdvertisementStatusChoices

MAX_OPEN_ADS_PER_USER = 10

class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'updated_at','created_at', )
        read_only_fields = ('creator', 'created_at', 'updated_at')

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        user = self.context["request"].user
        # Проверяем только для аутентифицированных пользователей (хотя права должны это сделать раньше)
        if not user.is_authenticated:
            return data

        # Определяем, какой статус будет у объявления после операции
        # Если статус не передается при обновлении, берем текущий статус объекта
        requested_status = data.get('status', None)
        is_creating = self.instance is None # Определяем, создание это или обновление

        final_status = requested_status
        if not is_creating and requested_status is None:
            # При PATCH запросе статус может не передаваться, берем текущий
             final_status = self.instance.status
        elif is_creating and requested_status is None:
             # При создании, если статус не указан, он будет OPEN по умолчанию (из модели)
             final_status = AdvertisementStatusChoices.OPEN

        # Валидация срабатывает, только если итоговый статус - OPEN
        if final_status == AdvertisementStatusChoices.OPEN:
            # Считаем текущие открытые объявления пользователя
            open_ads_count = Advertisement.objects.filter(
                creator=user, status=AdvertisementStatusChoices.OPEN
            ).count()

            # Если это создание нового объявления и лимит уже достигнут
            if is_creating and open_ads_count >= MAX_OPEN_ADS_PER_USER:
                raise ValidationError(
                    f"Превышен лимит открытых объявлений ({MAX_OPEN_ADS_PER_USER})."
                    " Закройте старые объявления перед созданием нового."
                )

            # Если это обновление СУЩЕСТВУЮЩЕГО объявления (instance есть)
            # и мы пытаемся изменить статус НЕ-OPEN на OPEN,
            # а лимит уже достигнут.
            if not is_creating and self.instance.status != AdvertisementStatusChoices.OPEN and open_ads_count >= MAX_OPEN_ADS_PER_USER:
                 raise ValidationError(
                    f"Превышен лимит открытых объявлений ({MAX_OPEN_ADS_PER_USER})."
                    " Вы не можете открыть это объявление."
                )

        return data
