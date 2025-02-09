from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from .models import Report
from .serializers import ReportSerializer

class ReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for generating and managing financial reports.
    Users can only see their own reports.
    """
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Staff can see all reports.
        Regular users can only see their own reports.
        """
        if self.request.user.is_staff:
            return Report.objects.all()
        return Report.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        format = self.request.data.get("format", "pdf") # Default format is PDF

        if format not in ['pdf', 'excel']:
            raise PermissionDenied("Invalid format. Choose 'pdf' or 'excel'.")
        
        file_content = b"Test content" # Test content
        file_name = f"report_{self.request.user.id}_{format}.{'pdf' if format == 'pdf' else 'xlsx'}"

        report = serializer.save(user=self.request.user, format=format)

        # Save file to the model
        report.file.save(file_name, ContentFile(file_content))



"""
Possíveis Melhorias
    Implementar geração real de relatórios

    Atualmente, o arquivo gerado é falso ("Test content").
    Podemos usar bibliotecas como ReportLab (para PDF) e openpyxl (para Excel).
    Adicionar filtros por data

    Permitir que o usuário filtre relatórios por intervalo de tempo.
    Enviar relatório por e-mail automaticamente

    Gerar e enviar o relatório para o e-mail do usuário após a criação.
"""
