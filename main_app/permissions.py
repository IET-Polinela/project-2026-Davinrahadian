from rest_framework.permissions import BasePermission


class IsReportOwnerAndDraft(BasePermission):
    message = 'Hanya pemilik laporan dengan status DRAFT yang boleh mengubah atau menghapus laporan ini.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        return obj.reporter == request.user and obj.status == 'DRAFT'
