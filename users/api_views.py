from django.db import connection, transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserPublicOut, UserPrivateOut, UserUpdateIn
from . import sql_queries as q


def row_to_public(u):
    return {
        "username": u["username"],
    }


class MeView(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request):
        with connection.cursor() as cur:
            cur.execute(
                """
                        SELECT id, username, email
            FROM PawsUser WHERE id=%s
                """,
                [request.user.id],
            )
            cols = [c[0] for c in cur.description]
            row = cur.fetchone()
        if not row:
            return Response({"detail": "Not found."}, status=404)
        data = dict(zip(cols, row))
        return Response(UserPrivateOut().to_representation(data))

    def patch(self, request):
        ser = UserUpdateIn(data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        if not ser.validated_data:
            return Response(status=204)
        sets, params = [], []
        for k, v in ser.validated_data.items():
            sets.append(f"{k}=%s")
            params.append(v)
        params.append(request.user.id)
        with transaction.atomic(), connection.cursor() as cur:
            cur.execute(f"UPDATE PawsUser SET {', '.join(sets)} WHERE id=%s", params)
        return self.get(request)


class PublicProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username):
        with connection.cursor() as cur:
            cur.execute(
                """
                        SELECT username
                        FROM PawsUser WHERE username=%s)
                        """,
                [username],
            )
            cols = [c[0] for c in cur.description]
            row = cur.fetchone()
        if not row:
            return Response({"detail": "Not found."}, status=404)
        data = dict(zip(cols, row))
        return Response(UserPublicOut().to_representation(data))
