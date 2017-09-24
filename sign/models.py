from django.db import models

# Create your models here.
class Event(models.Model):
    #发布会表
    name = models.CharField(max_length=100) #发布会标题
    limit = models.IntegerField()#参加人数
    status = models.BooleanField()#状态
    address = models.CharField(max_length=200)#地址
    start_time = models.DateTimeField('events time')#发布会时间
    create_time = models.DateTimeField(auto_now=True)#创建时间（自动获取时间 当前时间）

    def __str__(self):
        return self.name

class Guest(models.Model):
    event = models.ForeignKey(Event)#关联发布会主键
    realname = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    sign = models.BooleanField() #签到状态
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event','phone') #联合主键

    def __str__(self):
        return self.realname

