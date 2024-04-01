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
        'POST': "新建",
        'PUT': "修改",
        'GET': "查询",
        'DELETE': "删除"
    }

    title = {
        'POST': '检查新建{name}时{param}字段有效值无效值测试',

    }

    content = {
        'content': '步骤{step}，通过接口{api}{method}{name}时，参数{param}为{range}【check{step}】',
        'checks': '【check{step}】{result}'
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