import json
import requests
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from MyAPP.models import DB_tucao, DB_home_href, DB_project, DB_apis


@login_required
def welcome(request):
    # return HttpResponse("hello")
    return render(request, "welcome.html")


# 自带的登陆态检查装饰符login_required
@login_required
def home(request):
    return render(request, "welcome.html", {"whichHTML": "home.html", "oid": ""})


def child_json(eid, oid=''):
    res = {}
    if eid == 'home.html':
        data = DB_home_href.objects.all()
        res = {
            "hrefs": data
        }
    if eid == 'project_list.html':
        data = DB_project.objects.all()
        res = {
            "projects": data,
        }
    if eid == 'P_apis.html':
        project = DB_project.objects.filter(id=oid)[0]
        apis = DB_apis.objects.filter(project_id=oid)
        res = {"project": project, "apis": apis}

    if eid == 'P_cases.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {"project": project}

    if eid == 'P_project_set.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {"project": project}

    return res


# 返回子页面
def child(request, eid, oid):
    print(eid)
    # return render(request, eid)
    res = child_json(eid, oid)
    return render(request, eid, res)


def login(request):
    return render(request, "login.html")


def login_action(request):
    u_name = request.GET["username"]
    p_word = request.GET["password"]
    print(u_name, p_word)
    # 使用authenticate（）方法，得到一个User对象，做user验证，
    user_obj = auth.authenticate(username=u_name, password=p_word)
    # 如果有这个用户,跳转到index页面
    if user_obj is not None:
        # 进行正确的动作
        # return HttpResponseRedirect("/home/")
        auth.login(request, user_obj)
        # request.session["user"] = u_name
        return HttpResponse("成功")
    else:
        # 进行错误的动作
        return HttpResponse("失败")


def register_action(request):
    u_name = request.GET["username"]
    p_word = request.GET["password"]
    # 开始联通django用户表
    from django.contrib.auth.models import User
    try:
        # 把用户输入的用户名和密码存到数据库，但django做了一次加密，
        # 所以就不能直接用，create的方法，要用User表的方法，create_user()
        user = User.objects.create_user(username=u_name, password=p_word)
        user.save()
        return HttpResponse("注册成功")
    except:
        return HttpResponse("注册失败,用户名已存在")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


def pei(request):
    tucao = request.GET["tucao_text"]
    DB_tucao.objects.create(user=request.user.username, text=tucao)
    return HttpResponse("123")


def api_help(request):
    return render(request, "welcome.html", {"whichHTML": "help.html", "oid": ""})


def project_list(request):
    return render(request, "welcome.html", {"whichHTML": "project_list.html", "oid": ""})


def delete_project(request):
    id = request.GET["id"]
    DB_project.objects.filter(id=id).delete()
    DB_apis.objects.filter(project_id=id).delete()
    return HttpResponse("")


def add_project(request):
    project_name = request.GET["project_name"]
    user = request.user.username
    DB_project.objects.create(name=project_name, remark="", user=user, other_user="")
    return HttpResponse("")


def open_apis(request, id):
    project_id = id
    return render(request, "welcome.html", {"whichHTML": "P_apis.html", "oid": project_id})


def open_cases(request, id):
    project_id = id
    return render(request, "welcome.html", {"whichHTML": "P_cases.html", "oid": project_id})


def open_project_set(request, id):
    project_id = id
    return render(request, "welcome.html", {"whichHTML": "P_project_set.html", "oid": project_id})


def save_project_set(request, id):
    project_id = id
    name = request.GET["name"]
    remark = request.GET["remark"]
    other_user = request.GET["other_user"]
    DB_project.objects.filter(id=project_id).update(name=name, remark=remark, other_user=other_user)
    return HttpResponse("")


def project_api_add(request, id):
    project_id = id
    DB_apis.objects.create(project_id=project_id,api_method='none')
    return HttpResponseRedirect("/apis/%s" % project_id)


def project_api_del(request, id):
    project_id = DB_apis.objects.filter(id=id)[0].project_id
    DB_apis.objects.filter(id=id).delete()
    return HttpResponseRedirect("/apis/%s" % project_id)


def save_bz(request):
    api_id = request.GET["api_id"]
    bz_value = request.GET["bz_value"]
    DB_apis.objects.filter(id=api_id).update(des=bz_value)
    return HttpResponse("")


def get_bz(request):
    api_id = request.GET["api_id"]
    bz_value = DB_apis.objects.filter(id=api_id)[0].des
    return HttpResponse(bz_value)


def Api_save(request):
    api_name = request.GET["api_name"]
    api_id = request.GET["api_id"]
    ts_method = request.GET["ts_method"]
    ts_url = request.GET["ts_url"]
    ts_host = request.GET["ts_host"]
    ts_header = request.GET["ts_header"]
    ts_body_method = request.GET["ts_body_method"]
    print(ts_body_method)
    print(ts_url)
    print(type(ts_url))
    print(ts_host)
    print(type(ts_host))
    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body
    else:
        ts_api_body = request.GET["ts_api_body"]

    # 保存数据
    DB_apis.objects.filter(id=api_id).update(name=api_name,
                                             api_method=ts_method,
                                             api_url=ts_url,
                                             api_header=ts_header,
                                             api_host=ts_host,
                                             body_method=ts_body_method,
                                             api_body=ts_api_body)
    return HttpResponse("success")


def get_api_data(request):
    # 第一句是获取到前端过来的接口id
    # 第二句是拿到这个接口的字典格式数据
    # 第三句是返回给前端，但是数据要变成json串。
    api_id = request.GET["api_id"]
    api = DB_apis.objects.filter(id=api_id).values()[0]
    return HttpResponse(json.dumps(api), content_type='application/json')


def Api_send(request):
    # 提取所有数据
    ts_api_name = request.GET["api_name"]
    api_id = request.GET["api_id"]
    ts_method = request.GET["ts_method"]
    ts_url = request.GET["ts_url"]
    ts_host = request.GET["ts_host"]
    ts_header = request.GET["ts_header"]
    ts_body_method = request.GET["ts_body_method"]

    if ts_body_method == "返回体":
        print("进入返回体逻辑")
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body
        if ts_body_method in ["", None]:
            return HttpResponse("请先选择好请求提编码格式和请求体，再点击Send发送请求！")
    else:
        print("进入正常逻辑")
        ts_api_body = request.GET["ts_api_body"]
        api = DB_apis.objects.filter(id=api_id)
        api.update(last_body_method=ts_body_method, last_api_body=ts_api_body)

    # 发送请求获取返回值
    header = json.loads(ts_header)  # 处理header

    # 拼接完整url
    if ts_host[-1] == '/' and ts_url[0] == '/':  # 都有/
        url = ts_host[:-1] + ts_url
    elif ts_host[-1] != '/' and ts_url[0] != '/':  # 都没有/
        url = ts_host + '/' + ts_url
    else:
        url = ts_host + ts_url  # 有一个/

    if ts_body_method == 'none':
        res = requests.request(ts_method.upper(), url, headers=header, data={})

    elif ts_body_method == "form-data":
        files = []
        payload = {}
        for i in eval(ts_api_body):
            payload[i[0]] = i[1]
        res = requests.request(ts_method.upper(), url, headers=header, data=payload, files=files)

    elif ts_body_method == "x-www-form-urlencoded":
        header["Content-Type"] = 'application/x-www-form-urlencoded'

        payload = {}
        for i in eval(ts_api_body):
            payload[i[0]] = i[1]
        res = requests.request(ts_method.upper(), url, headers=header, data=payload)
    else:
        if ts_body_method == 'Text':
            header["Content-Type"] = 'text/plain'
        if ts_body_method == 'JavaScript':
            header["Content-Type"] = 'text/plain'

        if ts_body_method == 'Json':
            header["Content-Type"] = 'text/plain'
        if ts_body_method == 'Html':
            header["Content-Type"] = 'text/plain'
        if ts_body_method == 'Xml':
            header["Content-Type"] = 'text/plain'
        res = requests.request(ts_method.upper(), url, headers=header, data=ts_api_body.encode('utf-8'))

    # 把返回值传递给前端页面
    # return HttpResponse("{'code':200}")
    return HttpResponse(res.text)
