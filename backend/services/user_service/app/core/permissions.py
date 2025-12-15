from .roles import Roles  # noqa


class Permissions:
    USERS_READ = "users.read"
    USERS_UPDATE = "users.update"
    USERS_DELETE = "users.delete"

    DEFECTS_CREATE = "defects.create"
    DEFECTS_UPDATE = "defects.update"
    DEFECTS_ASSIGN = "defects.assign"

    REPORTS_VIEW = "reports.view"


ROLE_PERMISSIONS = {
    Roles.ADMIN: {
        Permissions.USERS_READ,
        Permissions.USERS_UPDATE,
        Permissions.USERS_DELETE,
        Permissions.DEFECTS_CREATE,
        Permissions.DEFECTS_UPDATE,
        Permissions.DEFECTS_ASSIGN,
        Permissions.REPORTS_VIEW,
    },
    Roles.MANAGER: {
        Permissions.DEFECTS_ASSIGN,
        Permissions.DEFECTS_UPDATE,
        Permissions.REPORTS_VIEW,
    },
    Roles.ENGINEER: {
        Permissions.DEFECTS_CREATE,
        Permissions.DEFECTS_UPDATE,
    },
    Roles.VIEWER: {
        Permissions.REPORTS_VIEW,
    },
}
