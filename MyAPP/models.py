from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class DB_tucao(models.Model):
    # 用户
    user = models.CharField(max_length=30, null=True)
    # 内容
    text = models.CharField(max_length=200, null=True)
    # 时间
    ctime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text + str(self.ctime)


# 超链接传送门表
class DB_home_href(models.Model):
    name = models.CharField(max_length=30, null=True)
    href = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name + self.href


# 项目列表
class DB_project(models.Model):
    name = models.CharField(max_length=300, null=True)
    remark = models.CharField(max_length=1000, null=True)
    user = models.CharField(max_length=100, null=True)
    other_user = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class DB_apis(models.Model):
    project_id = models.CharField(max_length=10, null=True)  # 项目id
    name = models.CharField(max_length=100, null=True)  # 接口名字
    api_method = models.CharField(max_length=10, null=True)  # 请求方式
    api_url = models.CharField(max_length=1000, null=True)  # url
    api_header = models.CharField(max_length=1000, null=True)  # 请求头
    api_login = models.CharField(max_length=10, null=True)  # 是否带登陆态
    api_host = models.CharField(max_length=100, null=True)  # 域名
    des = models.CharField(max_length=100, null=True)  # 描述
    body_method = models.CharField(max_length=20, null=True)  # 请求体编码格式
    api_body = models.CharField(max_length=1000, null=True)  # 请求体
    result = models.TextField(null=True)  # 返回体 因为长度巨大，所以用大文本方式存储
    sign = models.CharField(max_length=10, null=True)  # 是否验签
    file_key = models.CharField(max_length=50, null=True)  # 文件key
    file_name = models.CharField(max_length=50, null=True)  # 文件名
    public_header = models.CharField(max_length=1000, null=True)  # 全局变量-请求头
    last_body_method = models.CharField(max_length=20, null=True)  # 上次请求体编码格式
    last_api_body = models.CharField(max_length=1000, null=True)  # 上次请求头

    def __str__(self):
        return self.name


class DB_apis_log(models.Model):
    user_id = models.CharField(max_length=10, null=True)  # 所属用户id
    api_method = models.CharField(max_length=10, null=True)  # 请求方式
    api_url = models.CharField(max_length=1000, null=True)  # url
    api_header = models.CharField(max_length=1000, null=True)  # 请求头
    api_login = models.CharField(max_length=10, null=True)  # 是否带登陆态
    api_host = models.CharField(max_length=100, null=True)  # 域名
    des = models.CharField(max_length=100, null=True)  # 描述
    body_method = models.CharField(max_length=20, null=True)  # 请求体编码格式
    api_body = models.CharField(max_length=1000, null=True)  # 请求体
    sign = models.CharField(max_length=10, null=True)  # 是否验签
    file_key = models.CharField(max_length=50, null=True)  # 文件key
    file_name = models.CharField(max_length=50, null=True)  # 文件名

    def __str__(self):
        return self.api_url


class DB_cases(models.Model):
    project_id = models.CharField(max_length=30, null=True)  # 项目id
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class DB_step(models.Model):
    Case_id = models.CharField(max_length=10, null=True)  # 所属大用例id
    name = models.CharField(max_length=50, null=True)  # 步骤名字
    index = models.IntegerField(null=True)  # 执行步骤
    api_method = models.CharField(max_length=10, null=True)  # 请求方式
    api_url = models.CharField(max_length=1000, null=True)  # url
    api_host = models.CharField(max_length=100, null=True)  # host
    api_header = models.CharField(max_length=1000, null=True)  # 请求头
    api_body_method = models.CharField(max_length=10, null=True)  # 请求体编码类型
    api_body = models.CharField(max_length=10, null=True)  # 请求体
    get_path = models.CharField(max_length=500, null=True)  # 提取返回值-路径法
    get_zz = models.CharField(max_length=500, null=True)  # 提取返回值-正则
    assert_zz = models.CharField(max_length=500, null=True)  # 断言返回值-正则
    assert_qz = models.CharField(max_length=500, null=True)  # 断言返回值-全文检索存在
    assert_path = models.CharField(max_length=500, null=True)  # 断言返回值-路径法

    def __str__(self):
        # return str(self.id)     # 改成字符串的id
        return self.name