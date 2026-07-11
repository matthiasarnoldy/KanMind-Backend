from rest_framework import permissions

class IsBoardMemberOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        try:
            # Owner prüfen
            if obj.owner == request.user:
                return True
            # Mitglied prüfen (M2M)
            return request.user in obj.members.all()
        except Exception:
            return False