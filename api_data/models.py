from django.db import models
from django.conf import settings
import uuid
from django.contrib.auth.models import User
from django.db.models.base import Model
# Create your models here.
class apiStoreModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    dev_api = models.CharField(max_length=550)
    medium_api = models.CharField(max_length=550)
    hashnode_api = models.CharField(max_length=550)


class integrationModel(models.Model):
     id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
     user_id = models.IntegerField()
     notion_Oauth = models.CharField(max_length=550)
     notion_pg_id = models.CharField(max_length=550)
     notion_db_id = models.CharField(max_length=550)