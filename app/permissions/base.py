from app.models.user import User, UserRole
from app.permissions.roles import has_permission
from app.core.exceptions import ForbiddenException


class PermissionChecker:
    def check(self, user: User, permission: str) -> bool:
        if not user.is_active:
            raise ForbiddenException("User account is inactive")
        if not has_permission(user.role, permission):
            raise ForbiddenException(
                f"Role '{user.role}' cannot perform '{permission}'"
            )
        return True