import os, re, requests, json
import time
import unittest
from MyAPP.A_WQRFhtmlRunner import HTMLTestRunner


class Test(unittest.TestCase):
    def demo(self, step):
        time.sleep(3)
        # print("这是第一个测试类")
        print("步骤的url是%s" % step.api_url)
        # 提取所有的请求数据
        api_method = step.api_method
        api_url = step.api_url
        api_host = step.api_host
        api_header = step.api_header
        # print("api_header是{}".format(api_header))
        api_body_method = step.api_body_method
        api_body = step.api_body

        get_path = step.get_path
        get_zz = step.get_zz
        assert_path = step.assert_path
        assert_qz = step.assert_qz
        assert_zz = step.assert_zz

        # 检查是否需要进行替换占位符  得出来的结果时列表
        rlist_url = re.findall(r"##(.*?)##", api_url)
        for i in rlist_url:
            api_url = api_url.replace("##" + i + "##", str(eval(i)))

        rlist_header = re.findall(r"##(.*?)##", api_header)
        for i in rlist_header:
            api_header = api_header.replace("##" + i + "##", repr(str(eval(i))))

        # rlist_body = re.findall(r"##(.*?)##", api_body)
        # for i in rlist_body:
        #     api_body = api_url.replace("##" + i + "##", eval(i))

        if api_body_method == 'none':
            pass
        elif api_body_method == 'form-data' and api_body_method == 'x-www-form-urlencoded':
            rlist_body = re.findall(r"##(.*?)##", api_body)
            for i in rlist_body:
                api_body = api_body.replace("##" + i + "##", str(eval(i)))

        elif api_body_method == 'Json':
            rlist_body = re.findall(r"##(.*?)##", api_body)
            for i in rlist_body:
                api_body = api_body.replace("##" + i + "##", eval(repr(i)))

        else:
            rlist_body = re.findall(r"##(.*?)##", api_body)
            for i in rlist_body:
                api_body = api_body.replace("##" + i + "##", str(eval(i)))

        print("[host]:", api_host)
        print("[url]:", api_url)
        print("[header]:", api_header)
        print("[method]:", api_method)
        print("[body_method]:", api_body_method)
        print("[body]:", api_body)

        # 处理header
        try:
            header = json.loads(api_header)  # 处理header
        except:
            header = eval(api_header)

        # url 拼接
        if api_host[-1] == '/' and api_url[0] == '/':  # 都有/
            url = api_host[:-1] + api_url
        elif api_host[-1] != '/' and api_url[0] != '/':  # 都没有/
            url = api_host + '/' + api_url
        else:  # 肯定有一个有/
            url = api_host + api_url

        # 根据请求体类型发送请求
        if api_body_method == "none" or api_body_method == 'null':
            response = requests.request(api_method.upper(), url, headers=header)
        elif api_body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(api_body):
                payload[i[0]] = i[1]
            response = requests.request(api_method.upper(), url, headers=header, data=payload, files=files)
        elif api_body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(api_body):
                payload[i[0]] = i[1]
            response = requests.request(api_method.upper(), url, headers=header, data=payload)

        else:
            if api_body_method == 'Text':
                header["Content-Type"] = 'text/plain'
            if api_body_method == 'JavaScript':
                header["Content-Type"] = 'text/plain'

            if api_body_method == 'Json':
                header["Content-Type"] = 'text/plain'
            if api_body_method == 'Html':
                header["Content-Type"] = 'text/plain'
            if api_body_method == 'Xml':
                header["Content-Type"] = 'text/plain'
            # 把返回值传递给前端页面
            response = requests.request(api_method.upper(), url, headers=header, data=api_body.encode('utf-8'))
        response.encoding = "utf-8"
        res = response.text
        print("返回体：", res)
        # 对res 进行返回值提取

        # # 路径法提取：
        if get_path != '':
            # print("get_path 是%s" % get_path)
            # qid=/queryid
            for i in get_path.split("\n"):
                key = i.split("=")[0].rstrip()
                path = i.split("=")[1].lstrip()
                # path = /queryid
                py_path = ""
                for j in path.split("/"):
                    # 分成了["","queryid"]
                    if j != "":
                        # 如果不是空才会判断第一个字符是不是左中括号，
                        # 如果不是[开头，那说明是提取的是字典key，否则就是[数字]这样的列表下标。
                        if j[0] != '[':
                            py_path += '["%s"]' % j
                        else:
                            py_path += j
                # 调试
                # print(i)
                # print(py_path)
                # print("--------------")
                value = eval("%s%s" % (json.loads(res), py_path))
                # exec('self.%s=value' % key)
                exec('global %s\n%s = "%s"' % (key, key, value))

        # print(self.qid)
        # print(self.en)

        # # 正则法提取：
        if get_zz != '':
            for i in get_zz.split("\n"):
                key = i.split("=")[0].rstrip()
                zz = i.split("=")[1].lstrip()
                value = re.findall(zz, res)[0]
                # exec('self.%s = "%s"' % (key, value))
                exec('global %s\n%s="%s"' % (key, key, value))

        # print(self.z_en)
        # print(self.z_qid)

        # 对res 进行断言
        if assert_path != "":
            for i in assert_path.split("\n"):
                path = i.split("=")[0].rstrip()
                want = eval(i.split("=")[1].lstrip())
                py_path = ""
                for j in path.split("/"):
                    if j != "":
                        if j[0]!='[':
                            py_path += '["%s"]' %j
                        else:
                            py_path += j
                #           字典["key"]
                value = eval("%s%s" %(json.loads(res),py_path))

                self.assertEqual(want,value,"值不相等")

# 不理解
def make_defself(step):
    def tool(self):
        Test.demo(self, step)
        # 这个版本的htmltestrunner 中有方法注释显示在网页

    setattr(tool, "__doc__", u"%s" % step.name)
    return tool


def make_def(steps):
    for i in range(len(steps)):
        setattr(Test, "test" + str(steps[i].index).zfill(3), make_defself(steps[i]))


def run(Case_id, Case_name, steps):
    '''测试类'''
    print("我是step：{}".format(steps))
    make_def(steps)
    suite = unittest.makeSuite(Test)
    filename = "MyApp/templates/Reports/{}.html".format(Case_id)
    with open(filename, "wb") as f:
        runner = HTMLTestRunner(f, title="接口测试平台报告:%s" % Case_name, description="ai")
        runner.run(suite)


if __name__ == '__main__':
    unittest.main()
