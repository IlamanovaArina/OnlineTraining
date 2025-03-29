from rest_framework.permissions import BasePermission
import logging
from materials.models import Course, Lesson

logger = logging.getLogger(__name__)


class ModeratorPermission(BasePermission):
    """ Кастомное разрешение для модераторов """
    def has_permission(self, request, view):
        # Проверить, является ли пользователь модератором
        if request.user and request.user.groups.filter(name='moderator_training').exists():
            # Разрешить доступ к просмотру и изменению
            return bool(request.method in ['GET', 'PUT', 'PATCH'])

        # Запретить доступ для всех остальных
        return False


class IsOwner(BasePermission):
    """Класс ограничений по доступу для владельцев курсов и уроков."""

    def has_object_permission(self, request, view, obj):
        """Метод для проверки прав доступа у пользователя на объект."""

        if obj.owner == request.user:
            return True
        return False
