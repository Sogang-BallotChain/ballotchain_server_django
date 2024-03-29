from django.db import models

# Create your models here

from user.models import User

class Ballot (models.Model):
    name = models.CharField(max_length=128, verbose_name='투표 제목')
    candidate_list = models.TextField (verbose_name='후보자 리스트')
    voter_list = models.TextField (verbose_name='투표자 리스트', default="[]")
    start_time = models.IntegerField(verbose_name = '시작 시간')
    end_time = models.IntegerField(verbose_name = '종료 시간')
    address = models.TextField(verbose_name='Ethereum address', default="0x")

# 이메일 모델
class Verification(models.Model):
    email = models.EmailField(verbose_name = '이메일')
    code = models.TextField(verbose_name = '검증코드')
    start_time = models.IntegerField(verbose_name = '시작 시간')
    end_time = models.IntegerField(verbose_name = '종료 시간')