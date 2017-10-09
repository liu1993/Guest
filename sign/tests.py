from django.test import TestCase
from sign.models import Event,Guest
from django.contrib.auth.models import User
# Create your tests here.
class ModelTest(TestCase):
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

# class LoginActionTest(TestCase):
