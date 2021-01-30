import json
import requests
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from MyAPP.models import DB_tucao, DB_home_href, DB_project, DB_apis, DB_apis_log, DB_cases, DB_step


@login_required
def welcome(request):
    # return HttpResponse("hello")
    return render(request, "welcome.html")


# 自带的登陆态检查装饰符login_required
@login_required
def home(request):
    return render(request, "welcome.html", {"whichHTML": "home.html", "oid": request.user.id})


def child_json(eid, oid=''):
    res = {}
    if eid == 'home.html':
        data = DB_home_href.objects.all()
        home_log = DB_apis_log.objects.filter(user_id=oid)
        res = {
            "hrefs": data,
            "home_log": home_log
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
        project = DB_project.objects.filter(id= oid)[0]
        Cases = DB_cases.objects.filter(project_id=oid)
        apis = DB_apis.objects.filter(project_id=oid)
        for i in apis:
            print(i.id)
            print(i.name)
        res  = {"project":project,"Cases":Cases,"apis":apis}
        print(res)
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
    DB_apis.objects.filter(project_id=id).delete()  # 删除旗下接口
    DB_cases.objects.filter(project_id=id).delete()  # 删除旗下用例

    all_Case = DB_cases.objects.filter(project_id=id)
    for i in all_Case:
        DB_step.objects.filter(Case_id=i.id).delete()  # 删除步骤
        i.delete()  # 用例删除自己
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


def add_case(request, eid):
    DB_cases.objects.create(project_id=eid, name='这是新增的待修改用例')
    return HttpResponseRedirect("/cases/%s/" % eid)


def del_case(request, eid, oid):
    DB_cases.objects.filter(id=oid).delete()
    DB_step.objects.filter(Case_id=oid).delete()
    return HttpResponseRedirect("/cases/%s/" % eid)


def copy_case(request, eid, oid):
    old_case = DB_cases.objects.filter(id=oid)[0]
    DB_cases.objects.create(project_id=old_case.project_id, name=old_case.name + '_副本')
    return HttpResponseRedirect("/cases/%s/" % eid)


def get_small(request):
    case_id = request.GET["case_id"]
    steps = DB_step.objects.filter(Case_id=case_id).order_by("index")
    print(steps)
    res = {"all_steps": list(steps.values("index", "id", "name"))}
    print(res)
    print(type(res))
    return HttpResponse(json.dumps(res), content_type='application/json')


def add_new_step(request):
    case_id = request.GET["Case_id"]
    all_len = len(DB_step.objects.filter(Case_id=case_id))
    DB_step.objects.create(Case_id=case_id, name="我是新步骤", index=all_len + 1)
    return HttpResponse("")


def delete_step(request, eid):
    # DB_step.objects.filter(id=eid).delete()
    step = DB_step.objects.filter(id=eid)[0]  # 获取待删除的step
    index = step.index  # 获取目标index
    Case_id = step.Case_id  # 获取待删除的所属大用例id
    step.delete()  # 删除step
    for i in DB_step.objects.filter(Case_id=Case_id).filter(index__gt=index):
        # 遍历该大用例下所有序号大于目标index的step
        i.index -= 1  # 执行顺序自减1
        i.save()
    return HttpResponse("")


def get_step(request):
    step_id=request.GET["step_id"]
    step = DB_step.objects.filter(id=step_id)
    steplist=list(step.values())[0]
    print(steplist)
    return HttpResponse(json.dumps(steplist),content_type='application/json')



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
    DB_apis.objects.create(project_id=project_id, api_method='none')
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
    try:
        # 发送请求获取返回值
        header = json.loads(ts_header)  # 处理header
    except:
        return HttpResponse("请求头不符合json格式！")
    # 拼接完整url
    if ts_host[-1] == '/' and ts_url[0] == '/':  # 都有/
        url = ts_host[:-1] + ts_url
    elif ts_host[-1] != '/' and ts_url[0] != '/':  # 都没有/
        url = ts_host + '/' + ts_url
    else:
        url = ts_host + ts_url  # 有一个/
    try:
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
        res.encoding = 'utf-8'
        return HttpResponse(res.text)
    except Exception as e:
        return HttpResponse(str(e))


def copy_api(request):
    api_id = request.GET["api_id"]
    # 开始复制接口
    old_api = DB_apis.objects.filter(id=api_id)[0]
    DB_apis.objects.create(
        project_id=old_api.project_id,
        name=old_api.name + "_副本",
        api_method=old_api.api_method,
        api_url=old_api.api_url,
        api_header=old_api.api_header,
        api_login=old_api.api_login,
        api_host=old_api.api_host,
        des=old_api.des,
        body_method=old_api.body_method,
        api_body=old_api.api_body,
        result=old_api.result,
        sign=old_api.sign,
        file_key=old_api.file_key,
        file_name=old_api.file_name,
        public_header=old_api.public_header,
        last_body_method=old_api.last_body_method,
        last_api_body=old_api.last_api_body,
    )
    # 返回
    return HttpResponse("")


# def error_request(request):
#     api_id = request.GET["api_id"]
#     new_body = request.GET["new_body"]
#     print("==================================:{}".format(new_body))
#     api = DB_apis.objects.filter(id=api_id)[0]
#     method = api.api_method
#     url = api.api_url
#     host = api.api_host
#     header = api.api_header
#     body_method = api.body_method
#     header = json.loads(header)
#
#     # 拼接完整url
#     if host[-1] == '/' and url[0] == '/':  # 都有/
#         url = host[:-1] + url
#     elif host[-1] != '/' and url[0] != '/':  # 都没有/
#         url = host + '/' + url
#     else:
#         url = host + url  # 有一个/
#
#
#
#     if body_method == "form-data":
#         files = []
#         payload = {}
#         for i in eval(new_body):
#             payload[i[0]] = i[1]
#         res = requests.request(method.upper(), url, headers=header, data=payload, files=files)
#
#     elif body_method == "x-www-form-urlencoded":
#         header["Content-Type"] = 'application/x-www-form-urlencoded'
#
#         payload = {}
#         for i in eval(new_body):
#             payload[i[0]] = i[1]
#         res = requests.request(method.upper(), url, headers=header, data=payload)
#     elif body_method == 'Json':
#         header["Content-Type"] = 'text/plain'
#         res = requests.request(method.upper(), url, headers=header, data=new_body.encode('utf-8'))
#
#     else:
#         return HttpResponse("非法请求体类型")
#     # 把返回值传递给前端页面
#     # return HttpResponse("{'code':200}")
#     res.encoding = 'utf-8'
#     return HttpResponse(res.text)


# 异常值发送请求
def error_request(request):
    api_id = request.GET['api_id']
    new_body = request.GET['new_body']
    span_text = request.GET["span_text"]
    print(new_body)
    api = DB_apis.objects.filter(id=api_id)[0]
    method = api.api_method
    url = api.api_url
    host = api.api_host
    header = api.api_header
    body_method = api.body_method
    header = json.loads(header)
    if host[-1] == '/' and url[0] == '/':  # 都有/
        url = host[:-1] + url
    elif host[-1] != '/' and url[0] != '/':  # 都没有/
        url = host + '/' + url
    else:  # 肯定有一个有/
        url = host + url
    try:
        if body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
            response = requests.request(method.upper(), url, headers=header, data=payload, files=files)
        elif body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
            response = requests.request(method.upper(), url, headers=header, data=payload)
        elif body_method == 'Json':
            header['Content-Type'] = 'text/plain'
            response = requests.request(method.upper(), url, headers=header, data=new_body.encode('utf-8'))
        else:
            return HttpResponse('非法的请求体类型')
        # 把返回值传递给前端页面
        response.encoding = "utf-8"
        res_json = {"response": response.text, "span_text": span_text}
        # return HttpResponse(response.text)
        return HttpResponse(json.dumps(res_json), content_type="application/json")
    except:
        res_json = {"response": "对不起，接口异常", "span_text": span_text}
        return HttpResponse(json.dumps(res_json), content_type="application/json")
