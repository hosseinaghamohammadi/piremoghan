from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
# from django_quill.fields import QuillField
# from tinymce.models import HTMLField

class Major(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Person(AbstractUser):
    university_mail = models.CharField(max_length=70)
    university_id = models.IntegerField(verbose_name='student\'s id in university', unique=True, null=True)
    degree = models.CharField(max_length=50, blank=True)
    # major = models.ForeignKey(Major, on_delete=models.CASCADE, blank=True, null=True)
    # second_major = models.ForeignKey(Major, on_delete=models.CASCADE,)
    # minor = models.ForeignKey(Major, on_delete=models.CASCADE,)

    # profile_image = 

    blog_name = models.TextField(max_length=200)
    # blog_image = 
    # blog_color_theme = 
    
    ####################################### query-attributes
    # reading_history = 
    # year of studying
    # 
    def __str__(self):
        return self.first_name + " " + self.last_name

# class Article(models.Model):
#     STATUS = (("DRAFT", "Draft"), ("PUBLISHED", "Published"))

#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
#     title = models.TextField(max_length=80, null=True, blank=True)
#     text = models.TextField(blank=True)
#     tag = models.ManyToManyField(Tag, null=True, blank=True)

#     status = models.CharField(default="DRAFT", choices=STATUS, max_length=10, blank=True, null=True)

#     login_required = models.BooleanField(default=True, blank=True, help_text="Enable this if users must login before they can read this article.")
    
#     # followup_for = models.ManyToManyField('self', symmetrical=False, blank=True, help_text=_('Select any other articles that this article follows up on.'), related_name='followups')

#     created_date = models.DateTimeField(verbose_name='the time article was published', auto_now_add=True, null=True, blank=True)
#     modified_date = models.DateTimeField(verbose_name='the time article was edited', auto_now=True, null=True, blank=True)
    
#     allow_comments = models.BooleanField(default=True, blank=True, null=True)

    # images = 
    # tags = 
    # this might include کار دانشجویی، زندگی دانشجویی، کار، درس، تعامل، انتخاب، سلامت، ورزش، هنر، ادبیات

    def __str__(self):
        return self.title + self.text
    # def __str__(self):
    #     if len(str(self.title).split(' ')) <= 3:
    #         return self.author.first_name + ' wrote ' + self.title
    #     else:
    #         return self.author.first_name + ' wrote ' + ' '.join(str(self.title).split(' ')[:5]) + '...'


# class Comment(models.Model):
#     message = models.TextField(null=True)
#     post = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
#     parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, default=None, blank=True)
#     writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
#     created_date = models.DateTimeField(verbose_name='the time article was published', auto_now_add=True, null=True)
#     last_edit_date = models.DateTimeField(verbose_name='the time article was edited', auto_now=True, null=True)


#     def __str__(self):
#         return self.message



# class Attachment(models.Model):
#     upload_to = lambda inst, fn: 'attach/%s/%s/%s' % (datetime.now().year, inst.article.slug, fn)

#     article = models.ForeignKey(Article, related_name='attachments')
#     attachment = models.FileField(upload_to=upload_to)
#     caption = models.CharField(max_length=255, blank=True)

#     class Meta:
#         ordering = ('-article', 'id')

#     def __unicode__(self):
#         return u'%s: %s' % (self.article, self.caption)

#     @property
#     def filename(self):
#         return self.attachment.name.split('/')[-1]

#     @property
#     def content_type_class(self):
#         mt = mimetypes.guess_type(self.attachment.path)[0]
#         if mt:
#             content_type = mt.replace('/', '_')
#         else:
#             # assume everything else is text/plain
#             content_type = 'text_plain'

#         return content_type

