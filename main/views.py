import base64

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User


class SignupView(APIView):
    def post(self, request):
        failed_message = {
            "message": "Account creation failed",
            "cause": "required user_id and password"
        }
        try:
            user_id = request.data["user_id"]
            password = request.data["password"]
        except Exception:
            return Response(failed_message, status=400)

        len_user_id = len(user_id)
        len_password = len(password)
        if len_user_id < 6 or 20 < len_user_id:
            return Response(failed_message, status=400)
        if len_password < 6 or 20 < len_password:
            return Response(failed_message, status=400)

        # todo: user_id 半角英数字
        # todo: user_id 半角英数字記号（空白と制御コードを除くASCII文字)

        user = User.objects.filter(user_id=user_id).first()

        if user is not None:
            return Response({
                "message": "Account creation failed",
                "cause": "already same user_id is used"
            },
                            status=400)

        user = User.objects.create(
            user_id=user_id, password=password, nickname=user_id)

        return Response({
            "message": "Account successfully created",
            "user": {
                "user_id": user.user_id,
                "nickname": user.nickname,
            }
        },
                        status=200)


class UsersView(APIView):
    pass


class CloseView(APIView):
    def post(self, request):
        print(dir(request))
        print(request.META)
        print(request.META["HTTP_AUTHORIZATION"])
        values = request.META["HTTP_AUTHORIZATION"].split(' ')
        try:
            if values[0] != "Basic":
                raise Exception()
            user_id, password = base64.b64decode(
                values[1]).decode("utf8").split(":")
            print(user_id, password)
            user = User.objects.get(user_id=user_id, password=password)
            user.delete()
        except Exception:
            return Response({"message": "Authentication Faild"}, status=401)

        return Response({"message": "Account and user successfully removed"})
