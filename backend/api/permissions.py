from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


# class IsAdminUser(BasePermission):
#     def has_permission(self, request, view):
#         user = request.user
#         if user.is_anonymous:
#             return False
#         return bool(user and user.is_admin)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            if request.method in SAFE_METHODS:
                return True
            else:
                return False
        return (
            request.user.is_superuser
            or request.user.role == request.user.ADMIN
        )


# class IsAuthorOrAdminOrModerator(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method == "POST":
#             return not request.user.is_anonymous()

#         if request.method in ("PATCH", "DELETE"):
#             return (
#                 request.user == obj.author
#                 or request.user.role == request.user.ADMIN
#                 or request.user.role == request.user.MODERATOR
#             )

#         if request.method in SAFE_METHODS:
#             return True
#         return False