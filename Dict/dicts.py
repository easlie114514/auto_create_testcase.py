# -*- coding: utf-8 -*-
# @Time    : 2024/3/28 17:41
# @Author  : yanghangqiao / 杨杭桥
# @Email   : easlie.yang@dbappsecurity.com.cn
# @File    : dicts.py

class Dicts:
    def __init__(self):
        pass

    API = {
        'url': '/api/url',
        'name': 'api_name'

    }

    method = {
        '1': "POST",
        '2': "PUT",
        '3': "GET",
        '4': "DELETE"
    }

    title = {
        'POST': '检查新建{name}时{param}字段有效值无效值测试',
        'PUT': '检查修改{name}时{param}字段有效值无效值测试',
        'GET': '检查通过{url}获取',
        'DELETE': '检查删除{name}测试'
    }

    post_or_put_content = {
        'content': '步骤{step}，通过接口{api}{method}{name}时，参数{param}{type}{value}，其他参数为任意有效值【check{step}】',
        'checks': '【check{step}】{result}'
    }

    delete_content = {
        'content': '步骤{step}，通过接口{url}删除{name},{key}{state}',
        'checks': '【check{step}】{result}'
    }

    param_type = {
        'length': '长度',
        'value': '值',
        'custom': ''
    }

    result = {
        'success': 'success',
        'failure': 'failure'
    }

    cases = {

    }

    excel = {
        'A1': '用例标题',
        'B1': '用例步骤',
        'C1': '检查点'
    }