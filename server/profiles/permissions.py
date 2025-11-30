from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Permission to only allow owners to edit their own objects
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Write permissions only to owner
        return obj.user == request.user


class IsGuideOwner(BasePermission):
    """
    Permission to only allow guides to access their own profile
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "guide_profile")
            and request.user.is_guide
        )


class IsTouristOwner(BasePermission):
    """
    Permission to only allow tourists to access their own profile
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "tourist_profile")
            and request.user.is_tourist
        )
