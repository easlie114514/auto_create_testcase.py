# -*- coding: utf-8 -*-
# @Time    : 2024/3/28 17:40
# @Author  : yanghangqiao / 杨杭桥
# @Email   : easlie.yang@dbappsecurity.com.cn
# @File    : utils.py.py

import logging


class PublicUtil:
    @staticmethod
    def create_box(text):
        lines = text.split('\n')
        max_length = max(len(line) for line in lines)
        horizontal_line = '+' + '-' * (max_length + 2) + '+'
        boxed_text = [horizontal_line]
        for line in lines:
            boxed_text.append('| ' + line.ljust(max_length) + ' |')
        boxed_text.append(horizontal_line)
        return '\n'.join(boxed_text)


class SelectUtil:

    # 选择用于生成用例的key值
    @staticmethod
    def select_params(keys: list, selections: list):
        print('已识别所有key值如下')
        for index, value in enumerate(keys):
            print(str(index) + ': ' + value)
        while True:
            idxs = input('请选择需要使用的key值索引并重命名,以-1退出（例如1,2,3,-1）：\n').split(',')
            for idx in idxs:
                if int(idx) != -1:
                    if int(idx) < len(keys):
                        selections.append(input(f'{keys[int(idx)]}重命名为：'))
                    else:
                        logging.error(f'索引{idx}无效')
                else:
                    print('当前已选择参数')
                    print(selections)
                    return selections

    # 删除已选的key值
    @staticmethod
    def del_params(selections: list):
        while True:
            print('已选择参数如下：')
            for index, value in enumerate(selections):
                print(str(index) + ': ' + value)
            idxs = input('请选择需要删除的参数,以-1退出（例如1,2,3,-1）：\n').split(',')
            for idx in idxs:
                if int(idx) != -1:
                    if int(idx) < len(selections):
                        selections.remove(selections[int(idx)])
                        print('删除成功')
                    else:
                        logging.error(f'索引{idx}无效')
                else:
                    print('当前已选择参数')
                    print(selections)
                    return selections

    # 选择测试数据生成方式
    @staticmethod
    def select_method(selections: list):
        print('分别为已选择的参数选择方法以及对应值：')
        for seletion in selections:
            while True:
                methods = input(f'为字段{seletion}选择methods\n1-POST  2-PUT  3-GET  4-DELETE  0-exit').split(',')
                for method in methods:
                    if int(method) == 1:
                        case = int(input('1-等价类  2-边界值'))
                        if case == 1:
                            DataUtil.equivalent()
                        else:
                            DataUtil.border()


class DataUtil:

    # 获取JSON中所有key值
    def get_all_keys(self, json_data, keys_list=None):
        if keys_list is None:
            keys_list = []
        # 处理内嵌dict
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                keys_list.append(key)
                self.get_all_keys(value, keys_list)
        # 处理内嵌list
        if isinstance(json_data, list):
            for item in json_data:
                self.get_all_keys(item, keys_list)
        return keys_list

    # 根据给出的范围确定边界值
    @staticmethod
    def border():
        borders = input('请输入范围（例如：1-2,100-200）：').split(',')
        interval_list = [list(map(int, item.split('-'))) for item in borders]
        merged_interval = []
        for start, end in interval_list:
            merged = False
            for i in range(len(merged_interval)):
                if start <= merged_interval[i][1] and end >= merged_interval[i][0]:
                    merged_interval[i][0] = min(merged_interval[i][0], start)
                    merged_interval[i][1] = max(merged_interval[i][1], end)
                    merged = True
                    print('请不要试图找bug...')
                    break
            if not merged:
                merged_interval.append([start, end])
        final_border = list(filter(lambda x: x[0] <= x[1], merged_interval))
        print('已确认范围')
        print(final_border)

    # 根据给出的范围确定等价类
    @staticmethod
    def equivalent():
        return 1
