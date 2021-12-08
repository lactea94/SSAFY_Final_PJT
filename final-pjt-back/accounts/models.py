from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.deletion import CASCADE

import sys
sys.path.append('/server/movies')

from movies.models import Genre
class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    content = models.TextField()    
    genre = models.TextField()
