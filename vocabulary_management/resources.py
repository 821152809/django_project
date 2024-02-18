from import_export import resources
from .models import VocabularyManagement


class VocabularyManagementResource(resources.ModelResource):
    class Meta:
        model = VocabularyManagement
