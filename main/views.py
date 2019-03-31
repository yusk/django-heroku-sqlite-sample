import base64
import re

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User


def isalnum(s):
    # 半角英数字
    alnumReg = re.compile(r'^[a-zA-Z0-9]+$')
    return alnumReg.match(s) is not None


def isascii(s):
    # ASCII文字
    asciiReg = re.compile(r'^[!-~]+$')
    return asciiReg.match(s) is not None


def contain_control_char(s):
    return re.search(r"[\0-\037]", s)


def contain_space(s):
    return s.find(" ") >= 0


class SignupView(APIView):
    def post(self, request):
        print(request.data)
        try:
            user_id = request.data["user_id"]
            password = request.data["password"]
        except Exception:
            message = {
                "message": "Account creation failed",
                "cause": "required user_id and password"
            }
            return Response(message, status=400)

        len_user_id = len(user_id)
        len_password = len(password)
        if len_user_id < 6 or 20 < len_user_id:
            message = {
                "message": "Account creation failed",
                "cause": "bad user_id length"
            }
            return Response(message, status=400)
        if len_password < 6 or 20 < len_password:
            message = {
                "message": "Account creation failed",
                "cause": "bad password length"
            }
            return Response(message, status=400)

        if not isalnum(user_id):
            message = {
                "message": "Account creation failed",
                "cause": "bad user_id pattern"
            }
            return Response(message, status=400)

        if not isascii(password) or contain_control_char(
                password) or contain_space(password):
            message = {
                "message": "Account creation failed",
                "cause": "bad password pattern"
            }
            return Response(message, status=400)

        user = User.objects.filter(user_id=user_id).first()

        if user is not None:
            message = {
                "message": "Account creation failed",
                "cause": "already same user_id is used"
            }
            return Response(message, status=400)

        user = User.objects.create(
            user_id=user_id, password=password, nickname=user_id)

        return Response({
            "message": "Account successfully created",
            "user": {
                "user_id": user.user_id,
                "nickname": user.nickname,
            }
        })


class UsersView(APIView):
    def get(self, request, id):
        try:
            print(dir(request))
            print(request.META)
            print(request.META["HTTP_AUTHORIZATION"])
            values = request.META["HTTP_AUTHORIZATION"].split(' ')
            if values[0] != "Basic":
                raise Exception()
            user_id, password = base64.b64decode(
                values[1]).decode("utf8").split(":")
            print(user_id, password)
            User.objects.get(user_id=user_id, password=password)
        except Exception:
            return Response({"message": "Authentication Faild"}, status=401)

        try:
            user = User.objects.get(user_id=id)
        except Exception:
            return Response({"message": "No User found"}, status=404)

        res = {
            "message": "User details by user_id",
            "user": {
                "user_id": user.user_id,
                "nickname": user.nickname
            }
        }

        if user.comment is not None:
            res["user"]["comment"] = user.comment

        return Response(res)

    def patch(self, request, id):
        print(request.data)
        try:
            print(dir(request))
            print(request.META)
            print(request.META["HTTP_AUTHORIZATION"])
            values = request.META["HTTP_AUTHORIZATION"].split(' ')
            if values[0] != "Basic":
                raise Exception()
            user_id, password = base64.b64decode(
                values[1]).decode("utf8").split(":")
            print(user_id, password)
            User.objects.get(user_id=user_id, password=password)
        except Exception:
            return Response({"message": "Authentication Faild"}, status=401)

        if user_id != id:
            message = {"message": "No Permission for Update"}
            return Response(message, status=403)

        try:
            user = User.objects.get(user_id=id)
        except Exception:
            return Response({"message": "No User found"}, status=404)

        if "nickname" not in request.data and "comment" not in request.data:
            return Response({
                "message": "User updation failed",
                "cause": "required nickname or comment"
            },
                            status=400)

        if "user_id" in request.data or "password" in request.data:
            return Response({
                "message": "User updation failed",
                "cause": "not updatable user_id and password"
            },
                            status=400)

        try:
            nickname = request.data["nickname"]
            if len(nickname) > 30:
                message = {
                    "message": "User updation failed",
                    "cause": "bad nickname length"
                }
                return Response(message, status=400)
            if contain_control_char(nickname):
                message = {
                    "message": "User updation failed",
                    "cause": "bad nickname pattern"
                }
                return Response(message, status=400)
            if nickname == "":
                user.nickname = user.user_id
            else:
                user.nickname = nickname
        except Exception:
            pass

        try:
            comment = request.data["comment"]
            if len(comment) > 100:
                message = {
                    "message": "User updation failed",
                    "cause": "bad comment length"
                }
                return Response(message, status=400)
            if contain_control_char(comment):
                message = {
                    "message": "User updation failed",
                    "cause": "bad comment pattern"
                }
                return Response(message, status=400)
            if comment == "":
                user.comment = None
            else:
                user.comment = comment
        except Exception:
            pass

        user.save()

        return Response({
            "message": "User successfully updated",
            "user": {
                "nickname": user.nickname,
                "comment": user.comment
            }
        })


class CloseView(APIView):
    def post(self, request):
        print(request.data)
        try:
            print(dir(request))
            print(request.META)
            print(request.META["HTTP_AUTHORIZATION"])
            values = request.META["HTTP_AUTHORIZATION"].split(' ')
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
