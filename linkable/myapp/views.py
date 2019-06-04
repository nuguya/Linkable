from .models import Book, Recommend, MyUser
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from .rankalgoritm import rank
from .serializers import CreateUserSerializer, UserSerializer, BookSerializer, RecommendSerializer


@csrf_exempt
@api_view(['GET', 'POST'])
def select_book(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        user = request.user
        print(user)
    except Book.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'POST':
        append_book = book.node
        origin_recommend = Recommend.objects.get(username=user)
        if append_book in origin_recommend.books:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        origin_recommend.books.append(append_book)
        recommend = Recommend(username=origin_recommend.username, books=origin_recommend.books)
        serializer = RecommendSerializer(recommend)
        serializer = RecommendSerializer(origin_recommend, data=serializer.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        book.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'PUT'])
def book_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        book_list=Book.objects.all()
        serializer = BookSerializer(book_list, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def my_book(request):
    try:
        user = request.user
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET' and user is not None:
        mybook_serializer=RecommendSerializer(Recommend.objects.get(username=user))
        mybook = mybook_serializer.data.get('books')
        response_data=[]
        for i in mybook:
            print(i)
            response_data.append(Book.objects.get(node=i))

        response_serializer = BookSerializer(response_data,many=True)
        return Response(response_serializer.data)
    else:
        return Response(status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT'])
def recommend_book(request):
    try:
        user = request.user
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        tmp_list = []
        mybook_serializer = RecommendSerializer(Recommend.objects.get(username=user))
        mybook = mybook_serializer.data.get('books')
        r_value = rank(mybook)
        for i in range(0, 5):
            tmp_list.append(Book.objects.get(pk=r_value[i] + 1))
        serializer = BookSerializer(tmp_list, many=True)

        return Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def user_info(request):
    try:
        user = request.user
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET' and user is not None:
        userinfo = MyUser.objects.get_by_natural_key(username=user)
        user_serializer = UserSerializer(userinfo)

        return Response(user_serializer.data)


@csrf_exempt
@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
            body = {"message": "short field"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user1 = MyUser.objects.get_by_natural_key(username=request.data["username"])
        recommend = Recommend(username=user1)
        recommend.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
            }
        )
