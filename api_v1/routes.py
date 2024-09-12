from django.utils.dateparse import parse_date
from django.utils.timezone import now
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import generics
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from .models import HandBook, HandBookElement, VersionHandBook
from .serializers import (
    CheckElementSerializer,
    HandBookElementSerializer,
    HandBookSerializer,
)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name='date', description='Дата формата YYYY-mm-dd', type=str
            ),
        ],
        description='Получение списка справочников.\n\n Если указана дата, то актуальные на указанную дату',
    )
)
class AllHandBookAPI(generics.ListAPIView):
    serializer_class = HandBookSerializer

    def get_queryset(self):
        date_str = self.request.query_params.get('date', None)

        if date_str:
            try:
                date = parse_date(date_str)
            except ValueError:
                raise ValidationError(
                    {
                        'detail': "Некорректный формат даты. Используйте формат 'YYYY-MM-DD'."
                    }
                )

            if not date:
                raise ValidationError(
                    {
                        'detail': "Некорректный формат даты. Используйте формат 'YYYY-MM-DD'."
                    }
                )

            # отбросить справочники с версиями, где version_start_date > указанной дата
            return HandBook.objects.filter(
                versions__version_start_date__lte=date
            ).distinct()

        return HandBook.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer(queryset, many=True)
        return Response({'refbooks': serializer_class.data})


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='version', description='Версия', type=str),
        ],
        description='Получение элементов заданного справочника.\n\nЕсли не указана версия, то вернуться элементы текущей версии.',
    )
)
class HandBookElementListAPI(generics.ListAPIView):
    serializer_class = HandBookElementSerializer

    def get_queryset(self):
        handbook_id = self.kwargs.get('id')
        version_str = self.request.query_params.get('version', None)

        try:
            handbook = HandBook.objects.get(pk=handbook_id)
        except HandBook.DoesNotExist:
            raise NotFound('Справочник не найден.')

        if version_str:
            queryset = HandBookElement.objects.filter(
                version_hand_book__handbook=handbook,
                version_hand_book__version=version_str,
            )
            if not queryset.exists():
                raise NotFound('Данной версии для справочника не существует.')
        else:
            current_version = (
                VersionHandBook.objects.filter(
                    handbook=handbook, version_start_date__lte=now()
                )
                .order_by('-version_start_date')
                .first()
            )
            if current_version:
                queryset = HandBookElement.objects.filter(
                    version_hand_book__handbook=handbook,
                    version_hand_book__version=current_version.version,
                )
            else:
                queryset = HandBookElement.objects.none()

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'elements': serializer.data})


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name='code', description='Код', type=str, required=True
            ),
            OpenApiParameter(
                name='value', description='Значение', type=str, required=True
            ),
        ],
        description='Валидация элемента справочника.\n\n Проверка, что элемент с данным кодом и значением присутствует в указанной версии справочника.',
    )
)
class CheckElementAPI(generics.GenericAPIView):
    queryset = HandBook.objects.all()
    serializer_class = CheckElementSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        handbook_id = self.kwargs.get('id')
        code = serializer.validated_data.get('code')
        value = serializer.validated_data.get('value')
        version_str = serializer.validated_data.get('version', None)

        try:
            handbook = HandBook.objects.get(pk=handbook_id)
        except HandBook.DoesNotExist:
            raise NotFound('Справочник не найден.')

        if version_str:
            version_queryset = VersionHandBook.objects.filter(
                handbook=handbook, version=version_str
            )
        else:
            version_queryset = VersionHandBook.objects.filter(
                handbook=handbook, version_start_date__lte=now()
            ).order_by('-version_start_date')

        # проверить наличие версий
        if version_str and not version_queryset.exists():
            raise NotFound('Указанная версия не найдена.')
        elif not version_str and not version_queryset.exists():
            raise NotFound('Нет доступных версий для данного справочника.')

        current_version = (
            version_str if version_str else version_queryset.first().version
        )

        check_element = HandBookElement.objects.filter(
            version_hand_book__handbook=handbook,
            version_hand_book__version=current_version,
            uniq_code=code,
            value=value,
        ).exists()

        return Response({'status': check_element})
