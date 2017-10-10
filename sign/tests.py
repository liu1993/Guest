from django.test import TestCase
from sign.models import Event,Guest
from django.test import Client
from django.contrib.auth.models import User
from datetime import datetime
# Create your tests here.
class ModelTest(TestCase):
    '''测试model类（数据库）'''
    def setUp(self):
        Event.objects.create(id=1, name="oneplus 3 event", status=True, limit=2000,address='shenzhen', start_time='2016-08-31 02:18:22')
        Guest.objects.create(id=1,event_id=1,realname='alen',phone='13711001101',email='alen@mail.com', sign=False)

    def test_event_models(self):
        event = Event.objects.get(name='oneplus 3 event')
        self.assertEqual(event.address,'shenzhen')
        self.assertTrue(event.status)

    def test_guest_models(self):
        guest = Guest.objects.get(phone='13711001101')
        self.assertEqual(guest.realname,'alen')
        self.assertFalse(guest.sign)

class IndexPageTest(TestCase):
    '''测试index登录页'''
    def test_index(self):
        '''测试index视图'''
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')#只有使用render函数返回模板的才可以使用此断言

    def test_event_manage(self):
        response = self.client.get('http://127.0.0.1:8000/event_manage')
        self.assertEqual(response.status_code,301)
        # self.assertTemplateUsed(response,'event_manage.html')

class LoginActionTest(TestCase):
    '''测试登录函数'''
    def setUp(self):
        User.objects.create_user('admin','admin123456')
        self.c =Client()

    def test_login_action_username_password_null(self):
        '''用户名密码为空'''
        test_date = {'username':'','password':''}
        response = self.c.post('/login_action/',data=test_date)
        self.assertEqual(response.status_code,200)
        print(response.content)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_username_password_error(self):
        '''用户名密码错误'''
        test_date = {'username':'adm','password':''}
        response = self.c.post('/login_action/',data=test_date)
        self.assertEqual(response.status_code,200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
        '''登录成功'''
        test_date = {'username':'admin','password':'admin123456'}
        response = self.c.post('/login_action/',data=test_date)
        self.assertEqual(response.status_code,302)

class EventManageTest(TestCase):
    def setUp(self):
        Event.objects.create(id=2,name='xiaomi5',limit=2000,status=True,address='beijing',start_time=datetime(2016,8,10,14,0,0))
        self.c = Client()

    def test_event_manage_success(self):
        ''' 测试发布会:xiaomi5 '''
        response = self.c.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)





