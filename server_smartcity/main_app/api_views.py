from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly, IsCitizen


class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-updated_at')
    serializer_class = ReportSerializer
    pagination_class = ReportPagination

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Report.objects.none()

        tab = self.request.query_params.get('tab')
        base_queryset = self.queryset

        if tab == 'my_reports':
            return base_queryset.filter(reporter=user)

        if tab == 'feed':
            return base_queryset.filter(~Q(status='DRAFT')).exclude(reporter=user)

        # Default: semua laporan non-DRAFT ditampilkan, plus DRAFT milik user sendiri
        return base_queryset.filter(Q(status='DRAFT', reporter=user) | ~Q(status='DRAFT'))

    def get_permissions(self):
        if self.action == 'create':
            return [IsCitizen()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerAndDraftOrReadOnly()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)
