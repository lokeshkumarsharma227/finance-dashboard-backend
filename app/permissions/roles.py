from app.models.user import UserRole


ROLE_PERMISSIONS = {
    UserRole.VIEWER: [
        "read_records",
        "read_dashboard"
    ],
    UserRole.ANALYST: [
        "read_records",
        "read_dashboard",
        "create_records",
        "update_records"
    ],
    UserRole.ADMIN: [
        "read_records",
        "read_dashboard",
        "create_records",
        "update_records",
        "delete_records",
        "manage_users"
    ]
}


def has_permission(role: UserRole, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, [])