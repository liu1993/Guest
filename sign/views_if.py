from django.http import JsonResponse
from sign.models import Event
from sign.models import Guest
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db.utils import IntegrityError
import time


def add_event(request):

    # 添加发布会接口
    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')
    limit = request.POST.get('limit', '')
    status = request.POST.get('status', '')
    address = request.POST.get('address', '')
    start_time = request.POST.get('start_time', '')
    print('eid:%s' % eid)
    print('name:%s' % name)
    print('limit:%s' % limit)
    print('status:%s' % status)
    print('address:%s' % address)
    print('start_time:%s' % start_time)

    if eid == '' or name == '' or limit == ''or status == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'message': 'event id already exists'})

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': 'event name already exists'})

    if status == '':
        status = 1

    try:
        Event.objects.create(id=eid,name=name,limit=limit,status=status,address=address,start_time=start_time)
    except ValidationError as e:
        error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status': 200, 'message': 'add event success'})


def get_event_list(request):
    #发布会查询
    eid = request.GET.get('eid', '')
    name = request.GET.get('name', '')

    if eid == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['status_time'] = result.start_time
            return JsonResponse({'status': 200, 'message': 'success', 'data': event})

    if name != '':
        events = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event = {}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                events.append(event)
            return JsonResponse({'status': 200, 'message': 'success', 'data': events})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})


def add_guest(request):
    #添加嘉宾接口
    eid = request.POST.get('eid', '')  # 关联发布会 id
    realname = request.POST.get('realname', '')  # 姓名
    phone = request.POST.get('phone', '')  # 手机号
    email = request.POST.get('email', '')  # 邮箱

    if eid == '' or realname == '' or phone == '':
        return JsonResponse({'status': 10021,'message': 'parameter error'})

    result = Event.objects.get(id=eid)
    if not result:
        return JsonResponse({'status': 10022,'message': 'event id null'})

    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': 10023, 'message': 'event status is not available'})

    event_limit = Event.objects.get(id=eid).limit  # 发布会限制人数
    guest_limit = Guest.objects.filter(event_id=eid)  # 发布会已添加的嘉宾数
    if len(guest_limit) >= event_limit:
        return JsonResponse({'status': 10024, 'message': 'event number is full'})

    event_time = Event.objects.get(id=eid).start_time  # 发布会时间
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())  # 当前时间
    ntime = now_time.split(".")[0]
    n_time = int(ntime)

    if n_time >= e_time:
        return JsonResponse({'status': 10025, 'message': 'event has started'})

    try:
        Guest.objects.create(realname=realname, phone=int(phone), email=email, sign=0, event_id=int(eid))
    except IntegrityError:
        return JsonResponse({'status': 10026, 'message': 'the event guest phone number repeat'})

    return JsonResponse({'status': 200, 'message': 'add guest success'})


def get_guest_list(request):
    #嘉宾查询接口
    eid = request.POST.get('eid', '')
    phone = request.POST.get('phone','')

    if eid == '':
        return JsonResponse({'status': 10021, 'message': 'eid cannot be empty'})

    if eid != '' and phone == '':
        guests =[]
        results = Guest.objects.get(event_id=eid)
        if results:
            for r in results:
                guest = {}
                guest['realname'] = r.realname
                guest['phone'] = r.phone
                guest['email'] = r.email
                guest['sign'] = r.sign
                guests.append(guest)
            return JsonResponse({'status': 200, 'message': 'success', 'data': guests})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})

    if eid != '' and phone != '':
        guest = {}
        try:
            result = Guest.objects.get(phone=phone, event_id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022, 'message':'query result is empty'})
        else:
            guest['realname'] = result.realname
            guest['phone'] = result.phone
            guest['email'] = result.email
            guest['sign'] = result.sign
            return JsonResponse({'status': 200, 'message': 'success', 'data': guest})


def user_sign(request):
    #签到接口
    eid = request.POST.get('eid', '')  # 发布会 id
    phone = request.POST.get('phone', '')  # 嘉宾手机号
    if eid == '' or phone == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'event id null'})

    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': 10023, 'message': 'event status is not available'})

    event_time = Event.objects.get(id=eid).start_time  # 发布会时间
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())  # 当前时间
    ntime = now_time.split(".")[0]
    n_time = int(ntime)

    if n_time >= e_time:
        return JsonResponse({'status': 10024, 'message': 'event has started'})

    result = Guest.objects.filter(phone=phone)
    if not result:
        return JsonResponse({'status': 10025, 'message': 'user phone null'})

    result = Guest.objects.filter(event_id=eid, phone=phone)
    if not result:
        return JsonResponse({'status': 10026, 'message': 'user did not participate in the conference'})

    result = Guest.objects.get(event_id=eid, phone=phone).sign
    if result:
        return JsonResponse({'status': 10027, 'message': 'user has sign in'})
    else:
        Guest.objects.filter(event_id=eid,phone=phone).update(sign='1')
        return JsonResponse({'status': 200, 'message': 'sign success'})