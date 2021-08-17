from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.forms.models import model_to_dict
from django.views.generic import *
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

# from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework import exceptions
from rest_framework.exceptions import *
from rest_framework.views import exception_handler
from .serializers import *
from .models import Person, Article
from .forms import *
from rest_framework import serializers
from django.contrib.auth.models import Permission
# from rest_framework.exceptions import PermissionDenied

from django.views import defaults
from django.views.decorators.csrf import requires_csrf_token
# from django.models import User


class SignUpView(generics.CreateAPIView):
    serializer_class = StudentSignupSerializer
    template_name = 'blog/not_logged/home.html'
    renderer_classes = [TemplateHTMLRenderer]
    # permission_required = 'sdijklf'
    # list(Permission.objects.filter(user=0))
    # permission_classes = [DjangoModelPermissions]
    # queryset = Student.objects.none()
    # login_url = 'http://localhost:8000/feed/'
    # permission_denied_message = 'ooooooooooooooooohhhhhhhhhhhhhhhhhhhh'
    # raise_exception = True
    # return_403 = True


    def perform_create(self, serializer):
        return serializer.save()


    def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(self.request)
            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN
        exception_handler = self.get_exception_handler()
        context = self.get_exception_handler_context()
        response = exception_handler(exc, context)
        if response is None:
            self.raise_uncaught_exception(exc)

        response.exception = True
        
        # if 'CSRF' in response.data['detail']:
        #     try:
        #         raise serializers.ValidationError({"university_mail": "You are logged in!"})
        #     except ValidationError as e:
        #         exception_handler = self.get_exception_handler()
        #         context = self.get_exception_handler_context()
        #         response = exception_handler(e, context)
        #         if response is None:
        #             self.raise_uncaught_exception(e)
        #         print(response.data)
        #         return response
        # response = render_to_response('students/403.html')
        # response.status_code = 403
        print(response)
        return response
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            person = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            return person
        except:
            return serializer

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('feed/')
        else:
            return render(request, self.template_name, context={'form1': self.serializer_class})
    
    def post(self, request):
        print('--------------------------------------------------------\n\n\n\n')
        output = self.create(request)
        if isinstance(output, Person):
            return render(request, self.template_name, context={'form1': self.serializer_class, 'new_user': output})
        # elif 'CSRF' in output.data['detail']:
        #     return redirect('feed/')
        else:
            print(output)
            return render(request, self.template_name, context={'form1': output})
        


def user_login(request):
    # print(request.method == 'GET')
    form_class = LogInForm
    if request.method == 'POST':
        username = request.POST['uni_username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(to='/feed/')
        else:
            return render(request, 'blog/not_logged/login.html', context={'form': form_class})
    elif request.method == 'GET':
        return render(request, 'blog/not_logged/login.html', context={'form': form_class})
    # success_url = 'http://localhost:8000/'
    # template_name = 'students/not_logged/login.html'
    # print(form_class)

def user_logout(request):
    logout(request)
    return redirect(to='/')

def reset_password(request):
    return render(request, 'blog/not_logged/reset_password.html')

class Profile(LoginRequiredMixin,
    #   generic.FormView,
    #   generics.UpdateAPIView,
      generics.RetrieveUpdateAPIView):
    serializer_class = EditProfileSerializer
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'students/logged/profile.html'
    model = Person
    queryset = Person.objects.all()
    # lookup_field = 'username'
    # return render(request, 'students/logged/profile.html')
    def get(self, request):
        if request.method == 'GET':
            print('Gotcha')
        queryset = Person.objects.filter(username=request.user.username).values()
        # return render(request, context={"user": queryset},
        # template_name=self.template_name)
        return Response({'user': queryset})
    
    def put(self, request, *args, **kwargs):
        obj = Person.objects.get(username=request.user.username)
        for attribute in request.data:
            if request.data[attribute]:
                setattr(obj, attribute, request.data[attribute])
                obj.save()
        print(obj.degree)
        return self.get(request)
    
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = request.user
    #     print(instance.degree)
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}

    #     return self.get(request)    

class Feed(LoginRequiredMixin,
    #   generic.ListView,
      generics.ListAPIView):
    serializer_class = PostListSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blog/logged/feed.html'
    def get(self, request):
        queryset = Article.objects.get(id=len(Article.objects.all()))
        print(queryset)
        # v = str(queryset.text, 'utf-8')
        # return render(request, self.template_name, context={"articles": list(queryset)})
        return Response({'article': queryset.text})

class CreatePost(LoginRequiredMixin,
    #   generic.CreateView,
      generics.CreateAPIView):
    serializer_class = CreatePostSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blog/logged/ct.html'
    # queryset = Article.objects.all()
    def get(self, request):
        return Response({'form': CreatePostForm()})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(request.data['text'])
        a = Article(text=request.data['text'], title=request.data['title'])
        a.save()
        return self.get(request)

class EditPost(LoginRequiredMixin,
    #   generic.FormView,
    #   generics.UpdateAPIView,
      generics.RetrieveUpdateAPIView):
    serializer_class = EditPostSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blog/logged/edit_post.html'
    model = Article
    def get(self, request):
        if request.method == 'PUT':
            print('Got it WRONG!')
        queryset = self.model.objects.get(id=len(self.model.objects.all()))
        return Response({
            'article': queryset.text,
            'form': EditPostForm()
            })
    
    def post(self, request, *args, **kwargs):
        obj = self.model.objects.get(id=len(self.model.objects.all()))
        setattr(obj, 'title', request.data['title'])
        setattr(obj, 'text', request.data['text'])
        obj.save()
        return self.get(request)

class StudentView(viewsets.ModelViewSet):
    serializer_class = EditProfileSerializer
    queryset = Person.objects.all()


