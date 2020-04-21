from django.db import models
from datetime import datetime

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.EmailField(max_length=50,unique=True)
    user_name = models.CharField(max_length=100)
    user_date_created = models.DateTimeField(default=datetime.utcnow())

    def __str__(self):
        return self.user_email

class Skills(models.Model):
    skill_id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=50, unique=True)
    skill_description = models.CharField(max_length=200, unique=False, null=True)
    skill_date_created = models.DateTimeField(default=datetime.utcnow())

    def __str__(self):
        return self.skill_name

class SkillMap(models.Model):
    skillmap_user_id = models.ForeignKey(Users,on_delete=models.PROTECT )
    skillmap_skill_id = models.ForeignKey(Skills,on_delete=models.PROTECT)
    skillmap_level = models.IntegerField()

    class Meta:
        unique_together = ('skillmap_user_id', 'skillmap_skill_id')
