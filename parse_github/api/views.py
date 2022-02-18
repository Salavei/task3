from .models import GitItem, GitUser
from .serializers import GitItemSerialize, GitGiveLinkSerialize
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, status
from rest_framework_api_key.permissions import HasAPIKey
from .tasks import initial_scraper


class GitCreateForApi(mixins.CreateModelMixin, GenericViewSet):
    """
    Представление для запуска scrapy через АПИ
    """
    queryset = GitUser.objects.all()
    serializer_class = GitGiveLinkSerialize
    permission_classes = [HasAPIKey]

    def create(self, request, *args, **kwargs):
        if ('github.com' in (self.request.data['owner_link']).lower()):
            initial_scraper.delay(self.request.data['owner_name'])
            return Response(self.request.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'Error': 'Это ссылка не на гитхаб'}, status=status.HTTP_400_BAD_REQUEST)


class GitCreateUser(mixins.CreateModelMixin, GenericViewSet):
    """
    Через это scrapy добавляются данные
    Простейшая проверка ссылки на наличия слова github.com
    """
    queryset = GitUser.objects.all()
    serializer_class = GitGiveLinkSerialize
    permission_classes = [HasAPIKey]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if ('github.com' in (self.request.data['owner_link']).lower()):
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'Error': 'Это ссылка не на гитхаб'}, status=status.HTTP_400_BAD_REQUEST)


class GitCreateView(mixins.CreateModelMixin, GenericViewSet):
    """ Апи по сохранению данных о репозиториях пользователя (или проекта) """
    queryset = GitItem.objects.all()
    serializer_class = GitItemSerialize
    permission_classes = [HasAPIKey]


class GitGetAllView(ReadOnlyModelViewSet):
    """ Апи получения всех репозиториев """
    queryset = GitItem.objects.all()
    serializer_class = GitItemSerialize
    permission_classes = [HasAPIKey]


class GitGiveLinkView(ReadOnlyModelViewSet):
    """ Апи получения ссылок на страницы пользователей (или проектов) """
    queryset = GitUser.objects.all()
    serializer_class = GitGiveLinkSerialize
    permission_classes = [HasAPIKey]


class GitGetRepView(APIView):
    """ Апи получения репозиториев пользователя (или проекта) """
    queryset = GitItem.objects.all()
    serializer_class = GitItemSerialize
    permission_classes = [HasAPIKey]

    def get(self, request, *args, **kwargs):
        get_rep_user = GitItem.objects.filter(owner_id=self.kwargs.get('pk'))
        return Response(get_rep_user.values())


class GitIndividualStatView(APIView):
    """
            Индивидуальная статистика:
                Репозиторий с максимальным количеством коммитов (название репозитория - количество)
                Среднее количество звезд в репозиториях

    """
    permission_classes = [HasAPIKey]

    def get(self, request, *args, **kwargs):
        max_count_commit = \
            GitItem.objects.filter(owner=self.kwargs.get('pk')).values('name_rep', 'commit_count').order_by(
                '-commit_count')[
                0]
        average_stars = GitItem.objects.filter(owner=self.kwargs.get('pk')).values('stars').aggregate(Avg('stars'))
        return Response({'Репозиторий с максимальным количеством коммитов': max_count_commit,
                         'Среднее количество звезд в репозиториях': average_stars})


class GitOverallStatView(APIView):
    """
            Общая статистика:
                Количество пользователей(проектов)
                Общее количество репозиториев
                Среднее количество репозиториев
     """
    permission_classes = [HasAPIKey]

    def get(self, request, *args, **kwargs):
        user_count = GitUser.objects.all().count()
        count_repo = GitItem.objects.all().count()
        return Response({'Количество пользователей(проектов)': user_count, 'Общее количество репозиториев': count_repo,
                         'Среднее количество репозиториев': count_repo / user_count})
