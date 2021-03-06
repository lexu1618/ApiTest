import json
import requests
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from MyAPP.models import DB_tucao, DB_home_href, DB_project, DB_apis, DB_apis_log, DB_cases, DB_step, DB_project_header, \
    DB_host, DB_project_host, DB_login


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
        project_header = DB_project_header.objects.filter(project_id=oid)
        hosts = DB_host.objects.all()

        project_host = DB_project_host.objects.filter(project_id=oid)
        print("DB_project_host:", project_host)
        # print(" project_header 是 ",project_header)

        for i in apis:
            #  新增接口时，url是未定义类型，所以api界面加载会报错，AttributeError: 'NoneType' object has no attribute 'split'
            try:
                i.short_url = i.api_url.split("?")[0][:50]
            except:
                i.short_url = ""
        res = {"project": project, "apis": apis, "project_header": project_header,
               "hosts": hosts, "project_host": project_host}

    if eid == 'P_cases.html':
        project = DB_project.objects.filter(id=oid)[0]
        Cases = DB_cases.objects.filter(project_id=oid)
        apis = DB_apis.objects.filter(project_id=oid)
        project_header = DB_project_header.objects.filter(project_id=oid)
        hosts = DB_host.objects.all()
        project_host = DB_project_host.objects.filter(project_id=oid)
        # for i in apis:
        #     print(i.id)
        #     print(i.name)
        res = {"project": project, "hosts": hosts, "Cases": Cases, "apis": apis, "project_header": project_header,
               "project_host": project_host}
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


# 保存项目全局请求头
def save_project_header(request):
    project_id = request.GET['project_id']
    req_names = request.GET['req_names']
    req_keys = request.GET['req_keys']
    req_values = request.GET['req_values']
    req_ids = request.GET['req_ids']
    names = req_names.split(',')
    keys = req_keys.split(',')
    values = req_values.split(',')
    ids = req_ids.split(',')
    for i in range(len(ids)):
        if names[i] != '':
            if ids[i] == 'new':
                DB_project_header.objects.create(project_id=project_id, name=names[i], key=keys[i], value=values[i])
            else:
                DB_project_header.objects.filter(id=ids[i]).update(name=names[i], key=keys[i], value=values[i])
        else:
            try:
                DB_project_header.objects.filter(id=ids[i]).delete()
            except:
                pass
    return HttpResponse('')


# 保存项目全局域名
def save_project_host(request):
    project_id = request.GET['project_id']
    req_names = request.GET['req_names']
    req_hosts = request.GET["req_hosts"]

    req_ids = request.GET['req_ids']
    names = req_names.split(',')
    hosts = req_hosts.split(",")
    ids = req_ids.split(',')
    for i in range(len(ids)):
        if names[i] != '':
            if ids[i] == 'new':
                DB_project_host.objects.create(project_id=project_id, name=names[i], host=hosts[i])
            else:
                DB_project_host.objects.filter(id=ids[i]).update(name=names[i], host=hosts[i])
        else:
            try:
                DB_project_host.objects.filter(id=ids[i]).delete()
            except:
                pass
    return HttpResponse('')


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


def save_case_name(request):
    id = request.GET["id"]
    name = request.GET["name"]
    DB_cases.objects.filter(id=id).update(name=name)
    return HttpResponse("")


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
    step_id = request.GET["step_id"]
    step = DB_step.objects.filter(id=step_id)
    steplist = list(step.values())[0]
    print(steplist)
    return HttpResponse(json.dumps(steplist), content_type='application/json')


def save_step(request):
    step_id = request.GET['step_id']
    name = request.GET['name']
    index = request.GET['index']
    step_method = request.GET['step_method']
    step_url = request.GET['step_url']
    step_host = request.GET['step_host']
    step_header = request.GET['step_header']
    step_body_method = request.GET['step_body_method']
    step_api_body = request.GET['step_api_body']

    get_path = request.GET["get_path"]
    get_zz = request.GET["get_zz"]
    assert_path = request.GET["assert_path"]
    assert_qz = request.GET["assert_qz"]
    assert_zz = request.GET["assert_zz"]
    mock_res = request.GET["mock_res"]
    ts_project_headers = request.GET["ts_project_headers"]

    DB_step.objects.filter(id=step_id).update(name=name,
                                              index=index,
                                              api_method=step_method,
                                              api_url=step_url,
                                              api_host=step_host,
                                              api_header=step_header,
                                              api_body_method=step_body_method,
                                              api_body=step_api_body,

                                              get_path=get_path,
                                              get_zz=get_zz,
                                              assert_path=assert_path,
                                              assert_qz=assert_qz,
                                              assert_zz=assert_zz,
                                              mock_res=mock_res,
                                              public_header=ts_project_headers
                                              )
    return HttpResponse('')


def step_get_api(request):
    api_id = request.GET["api_id"]
    api = DB_apis.objects.filter(id=api_id).values()[0]
    return HttpResponse(json.dumps(api), content_type="application/json")


def open_project_set(request, id):
    project_id = id
    return render(request, "welcome.html", {"whichHTML": "P_project_set.html", "oid": project_id})


def Run_Case(request):
    Case_id = request.GET["Case_id"]
    Case = DB_cases.objects.filter(id=Case_id)[0]
    # Case2 = DB_cases.objects.filter(id=Case_id)

    # print("case2 是{}".format(Case2))
    # print(type(Case2))
    # print(Case_id)
    steps = DB_step.objects.filter(Case_id=Case_id)
    # print("我是传参step：{}".format(steps))
    from MyAPP.run_case import run
    run(Case_id, Case.name, steps)
    return HttpResponse("")


def look_report(request, eid):
    Case_id = eid
    return render(request, 'Reports/%s.html' % Case_id)


def save_project_set(request, id):
    project_id = id
    name = request.GET["name"]
    remark = request.GET["remark"]
    other_user = request.GET["other_user"]
    DB_project.objects.filter(id=project_id).update(name=name, remark=remark, other_user=other_user)
    return HttpResponse("")


def project_api_add(request, id):
    project_id = id
    DB_apis.objects.create(project_id=project_id, api_method='none', api_url="")
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
    ts_project_headers = request.GET["ts_project_headers"]
    print("ts_project_headers", ts_project_headers)
    # print(ts_body_method)
    # print(ts_url)
    # print(type(ts_url))
    # print(ts_host)
    # print(type(ts_host))
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
                                             api_body=ts_api_body,
                                             public_header=ts_project_headers)
    return HttpResponse("success")


def get_api_data(request):
    # 第一句是获取到前端过来的接口id
    # 第二句是拿到这个接口的字典格式数据
    # 第三句是返回给前端，但是数据要变成json串。
    api_id = request.GET["api_id"]
    api = DB_apis.objects.filter(id=api_id).values()[0]
    # print("api :",api)
    return HttpResponse(json.dumps(api), content_type='application/json')


# 调试层发送请求
def Api_send(request):
    # 提取所有数据
    ts_api_name = request.GET["api_name"]
    api_id = request.GET["api_id"]
    ts_method = request.GET["ts_method"]
    ts_url = request.GET["ts_url"]
    ts_host = request.GET["ts_host"]
    # if "全局域名" in ts_host:
    if ts_host[:4] == "全局域名":
        project_host_id = ts_host.split("-")[1]
        ts_host = DB_project_host.objects.filter(id=project_host_id)[0].host
    ts_header = request.GET["ts_header"]
    ts_body_method = request.GET["ts_body_method"]
    # 前段ajax 传过来的时候toString 转化为字符串了，这里要还原成数组
    ts_project_headers = request.GET["ts_project_headers"].split(",")

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

    for i in ts_project_headers:
        if i != "":  # 当选择完公共请求头后取消选择，然后再请求就会报错的问题：
            project_header = DB_project_header.objects.filter(id=i)[0]
            header[project_header.key] = project_header.value

    print("header :", header)

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

        DB_host.objects.update_or_create(host=ts_host)
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


def project_get_login(request):
    project_id = request.GET["project_id"]
    # print("project_id:",project_id)
    try:
        login = DB_login.objects.filter(project_id=project_id).values()[0]
    except:
        login = {}
    # print("login:",login)
    return HttpResponse(json.dumps(login), content_type='application/json')


def project_login_save(request):
    project_id = request.GET["project_id"]
    login_method = request.GET["login_method"]
    login_url = request.GET["login_url"]
    login_host = request.GET["login_host"]
    login_header = request.GET["login_header"]
    login_body_method = request.GET["login_body_method"]
    login_api_body = request.GET["login_api_body"]
    login_response_set = request.GET["login_response_set"]

    # 保存数据
    DB_login.objects.filter(project_id=project_id).update(
        api_method=login_method,
        api_url=login_url,
        api_header=login_header,
        api_host=login_host,
        body_method=login_body_method,
        api_body=login_api_body,
        set=login_response_set
    )
    # 返回
    return HttpResponse("success")


def project_login_send(request):
    # 第一步，获取前端数据
    login_method = request.GET['login_method']
    login_url = request.GET['login_url']
    login_host = request.GET['login_host']
    login_header = request.GET['login_header']
    login_body_method = request.GET['login_body_method']
    login_api_body = request.GET['login_api_body']
    login_response_set = request.GET['login_response_set']

    # 第二步，发送请求
    try:
        header = json.loads(login_header)  # 处理header
    except:
        return HttpResponse('请求头不符合json格式！')

    # 拼接完整url
    if login_host[-1] == '/' and login_url[0] == '/':  # 都有/
        url = login_host[:-1] + login_url
    elif login_host[-1] != '/' and login_url[0] != '/':  # 都没有/
        url = login_host + '/' + login_url
    else:  # 肯定有一个有/
        url = login_host + login_url
    try:
        if login_body_method == 'none':
            response = requests.request(login_method.upper(), url, headers=header, data={})
        elif login_body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(login_api_body):
                payload[i[0]] = i[1]
            response = requests.request(login_method.upper(), url, headers=header, data=payload, files=files)

        elif login_body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(login_api_body):
                payload[i[0]] = i[1]
            response = requests.request(login_method.upper(), url, headers=header, data=payload)

        elif login_body_method == 'GraphQL':
            header['Content-Type'] = 'application/json'
            query = login_api_body.split('*WQRF*')[0]
            graphql = login_api_body.split('*WQRF*')[1]
            try:
                eval(graphql)
            except:
                graphql = '{}'
            payload = '{"query":"%s","variables":%s}' % (query, graphql)
            response = requests.request(login_method.upper(), url, headers=header, data=payload)


        else:  # 这时肯定是raw的五个子选项：
            if login_body_method == 'Text':
                header['Content-Type'] = 'text/plain'

            if login_body_method == 'JavaScript':
                header['Content-Type'] = 'text/plain'

            if login_body_method == 'Json':
                header['Content-Type'] = 'text/plain'

            if login_body_method == 'Html':
                header['Content-Type'] = 'text/plain'

            if login_body_method == 'Xml':
                header['Content-Type'] = 'text/plain'
            response = requests.request(login_method.upper(), url, headers=header, data=login_api_body.encode('utf-8'))

        # 把返回值传递给前端页面
        response.encoding = "utf-8"
        DB_host.objects.update_or_create(host=login_host)
        res = response.json()


        # 第三步  对返回值进行提取
        get_res = "" # 声明提取结果存放
        for i in login_response_set.split("\n"):
            if i == "":
                continue
            else:
                i = i.replace(' ', '')
                key = i.split('=')[0]  # 拿出key
                path = i.split('=')[1]  # 拿出路径
                value = res
                for j in path.split('/')[1:]:
                    value = value[j]
                get_res += key + '="' + value + '"\n'

            # 第四步，返回前端

        end_res = {"response": response.text, "get_res": get_res}

        return HttpResponse(json.dumps(end_res), content_type='application/json')

    except Exception as e:

        end_res = {"response": str(e), "get_res": ''}

        return HttpResponse(json.dumps(end_res), content_type='application/json')
