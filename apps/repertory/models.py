from django.db import models
from pip._internal.utils.encoding import auto_decode


class labelClassify(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32,unique=True)

class label(models.Model):
    id = models.AutoField(primary_key=True)   # auto-increment, primary key
    label_name = models.CharField(max_length=32, unique=True)   # label name
    classify = models.ForeignKey(to='labelClassify', to_field='name',on_delete=models.SET_NULL, null=True)

class articleInfo(models.Model):
    id = models.AutoField(primary_key=True)
    article_name = models.CharField(max_length=32)
    label = models.ForeignKey(to='label', to_field='label_name', on_delete=models.SET_NULL, null=True)
    abstract = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

class articleContent(models.Model):
    id = models.AutoField(primary_key=True)
    article_id = models.ForeignKey(to='articleInfo', to_field='id', on_delete=models.SET_NULL, null=True)
    article_content = models.TextField()

class userInfo(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=22)
    password = models.CharField(max_length=32)  # 密码应该加密
    # 昵称
    # 注册信息
    # 最近登录时间
    # 在线时长
