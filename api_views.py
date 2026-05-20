from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly, IsCitizen

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    
    def get_permissions(self):
        # Hanya Citizen yang boleh membuat laporan (Tujuan 3b)
        if self.action == 'create':
            return [IsCitizen()]
        # Jika melakukan update atau delete, gunakan permission custom
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerAndDraftOrReadOnly()]
        # Untuk list dan detail cukup login saja
        return [permissions.IsAuthenticated()]
        
    def perform_create(self, serializer):
        # Otomatis set reporter ke user yang sedang login
        serializer.save(reporter=self.request.user)