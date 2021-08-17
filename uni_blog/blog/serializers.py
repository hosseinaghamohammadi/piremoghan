from rest_framework import serializers
from .models import Person, Article
import random
from django.core.mail import send_mail
from uni_blog.settings import EMAIL_HOST_USER
from rest_framework.response import Response
from rest_framework import status

class StudentSignupSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        print('validate function is CALLED!\n')
        dep_mail = attrs['university_mail']
        seen = False
        with open('/home/hp-laptop/Downloads/Study/code/uni_blog/uni_blog/blog/mem95.txt', 'r') as m:
            if dep_mail+'\n' in m.readlines():
                seen = True
        if not seen:
            raise serializers.ValidationError({"university_mail": "This mail was not in the list. Please check again."})
        if Person.objects.filter(university_mail=dep_mail):
            raise serializers.ValidationError({"university_mail": "You've already signed up!"})
        return attrs


    def create(self, request, *args, **kwargs):
        print('create function is CALLED!\n')
        dep_username = request['university_mail']
        password_length = random.randint(20, 40)
        password = ''
        for i in range(password_length):
            char = random.randint(55, 116)
            if char < 65:
                char = chr(char - 7)
            elif char < 91:
                char = chr(char)
            else:
                char = chr(char + 6)
            password += char
        user = Person(
            username = dep_username,
            email = dep_username + "@ce.sharif.edu",
            first_name = request['first_name'],
            last_name = request['last_name'],
            university_mail = dep_username
            )
        user.set_password(password)
        user.save()
        send_mail(
            'Bah Bah! Khosh Umadi! :)',
            'Your password is inside the brackets: (' + password + ').',
            EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
        return user
    class Meta:
        model = Person
        fields = ('university_mail', 'first_name', 'last_name',)

class EditProfileSerializer(serializers.ModelSerializer):
    # lookup_field = 'username'
    # def update(self, attrs):
    #     print(attrs)
    #     pass
    # def update(self, instance, validated_data):
    #     print('Hashem')
    #     return None
        # return super().update(instance, validated_data)
        
    class Meta:
        model = Person
        fields = ('university_mail',
                  'degree',
                  'blog_name',
                  'first_name',
                  'last_name'
                 )

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'text')

class EditPostSerializer(serializers.ModelSerializer):
    # lookup_field = 'username'
    # def update(self, attrs):
    #     print(attrs)
    #     pass
    # def update(self, instance, validated_data):
    #     print('Hashem')
    #     return None
        # return super().update(instance, validated_data)
    def update(self, instance, validated_data):
        # instance.text = validated_data.get(, instance.text)
        # instance.content = validated_data.get('content', instance.content)
        # instance.created = validated_data.get('created', instance.created)
        print('update worked!')
        return instance

    class Meta:
        model = Article
        fields = (
            'title',
            'text',
        )

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title',
                  'text',
                 )

