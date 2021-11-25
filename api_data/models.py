import uuid
from django.db import models
# Create your models here.
class apiStoreModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    dev_api = models.CharField(max_length=550, blank=True, null=True)
    medium_api = models.CharField(max_length=550, blank=True, null=True)
    hashnode_api = models.CharField(max_length=550, blank=True, null=True)


class integrationModel(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user_id = models.IntegerField()
    notion_Oauth = models.CharField(max_length=550)
    notion_pg_id = models.CharField(max_length=550)
    notion_db_id = models.CharField(max_length=550)
    sync_url = models.CharField(max_length=550, blank=True, null=True)
    