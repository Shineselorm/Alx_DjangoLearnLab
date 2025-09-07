from django.apps import AppConfig
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass  # Type annotations can be added here if needed


class RelationshipAppConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'
    name = 'relationship_app'
