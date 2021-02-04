"""ApiTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from MyAPP.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r"^welcome/$",welcome),
    re_path(r"^welcome/$", welcome),
    re_path(r"^home/$", home),
    # 1 from django.urls import re_path
    # 在Python正则表达式中，命名正则表达式组的语法是(?P<name>pattern)，组name的名称，并且 pattern是要匹配的模式。
    #
    # 还是以上图圈中的部分为例，也是可以用正则表达式来写的。如下：
    #
    # 1 re_path(r'^(\d+)/$',views.peopleList,name='peopleList'),
    # 这样也是可以匹配到views视图中的peopleList函数的形参的。
    #
    # 所以这两种使用方式在使用上根据实际情况自行使用。
    re_path(r"^child/(?P<eid>.+)/(?P<oid>.*)/$", child),
    re_path(r"^login/$", login),  # 进入登录页面
    re_path(r"^login_action/$", login_action),  # 登录
    re_path(r"^register_action/", register_action),  # 登录
    re_path(r"^accounts/login/$", login),  # 非登录状态跳转到登录页面
    re_path(r"^logout/$", logout),  # 退出
    re_path(r"^pei/$", pei),  # 匿名吐槽
    re_path(r"^help/$", api_help),  # 进入帮助文档
    re_path(r"^project_list/$", project_list),  # 进入项目列表
    re_path(r"^delete_project/$", delete_project),
    re_path(r"^add_project/$", add_project),
    re_path(r"^apis/(?P<id>.*)/$", open_apis),  # 进入接口库
    re_path(r"^cases/(?P<id>.*)/$", open_cases),  # 进入接口库
    re_path(r"^project_set/(?P<id>.*)/$", open_project_set),  # 进入接口库
    re_path(r"^save_project_set/(?P<id>.+)/$", save_project_set),
    re_path(r"^project_add_api/(?P<id>.*)/$", project_api_add),
    re_path(r"^project_api_del/(?P<id>.*)/$", project_api_del),
    re_path(r"^save_bz/$", save_bz),
    re_path(r"^get_bz/$", get_bz),
    re_path(r"^Api_save/$", Api_save),
    re_path(r"^get_api_data/$", get_api_data),
    re_path(r"^Api_send/$", Api_send),
    re_path(r"^copy_api/$", copy_api),
    re_path(r"^error_request/$", error_request),  # 调用异常测试接口
    re_path(r"^add_case/(?P<eid>.*)/$", add_case),  # 增加用例
    re_path(r"^del_case/(?P<eid>.*)/(?P<oid>.*)/$", del_case),  # 删除用例
    re_path(r"^copy_case/(?P<eid>.*)/(?P<oid>.*)/$", copy_case),  # 复制用例
    re_path(r"^get_small/$", get_small),  # 获取小用例步骤的列表数据
    re_path(r"^add_new_step/$", add_new_step),
    re_path(r"^delete_step/(?P<eid>.*)/$", delete_step),
    re_path(r"^get_step/$", get_step),  # 获取小步骤
    re_path(r"^save_step/$", save_step),  # 保存小步骤
    re_path(r"^step_get_api/$", step_get_api),
    re_path(r"^Run_Case/$", Run_Case),  # 运行大用例
    re_path(r"^look_report/(?P<eid>.*)/$", look_report),  # 查看报告
    re_path(r"^save_project_header/$", save_project_header),
    re_path(r"save_case_name/$", save_case_name),  # 保存用例的名字
    re_path(r"save_project_host/$", save_project_host),  # 保存全局域名
    re_path(r"project_get_login/$", project_get_login),  # 获取登录态接口
    re_path(r"project_login_save/$", project_login_save),  # 保存项目登录态接口
    re_path(r"project_login_send/$", project_login_send)  # 调试请求登录态接口
]
