# -*- coding: utf-8 -*-
# @Time    : 2024/3/28 17:40
# @Author  : yanghangqiao / 杨杭桥
# @Email   : easlie.yang@dbappsecurity.com.cn
# @File    : utils.py.py

import logging
import math
from Dict.dicts import Dicts


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

    @staticmethod
    def count_decimal_places(num):
        integer_part, decimal_part = math.modf(num)
        if decimal_part == 0:
            return 0
        else:
            return len(str(decimal_part).split('.')[1])


class SelectUtil:

    # 选择用于生成用例的key值
    @staticmethod
    def select_params(keys: list, selections: list):
        print('————\n已识别所有key值如下')
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
            print('————\n已选择参数如下：')
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
    def select_method(api_url: str, api_name: str, selections: list):
        print('————\n分别为已选择的参数选择方法以及对应值：')
        data_util = DataUtil()
        for selection in selections:
            methods = input(f'为字段【{selection}】选择methods\n1-POST  2-PUT  3-GET  4-DELETE  0-exit\n').split(',')
            for method in methods:
                if int(method) == 1:
                    case = int(input('————\n1-等价类  2-边界值'))
                    if case == 1:
                        print('请输入合法范围（例如：1-2,5,100-200）')
                        equivalence_classes = data_util.get_values(method=1)
                        print('用例标题：\n' + Dicts.title['POST'].format(name=Dicts.API['name'], param=selection))
                        for step in range(len(equivalence_classes)):
                            print(Dicts.content['content'].format(step=step, api=Dicts.API['name'], method='新增',
                                                                  name=Dicts.API['name'], param=selection,
                                                                  range=equivalence_classes[step][0]))
                            print(Dicts.content['checks'].format(step=step, result=equivalence_classes[step][1]))
                    else:
                        print('请输入有效等价类（例如：1-2,5,100-200）')
                        data_util.get_values(method=0)




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

    def get_values(self, method=1):
        borders = input().split(',')
        interval_list = [list(map(float, item.split('-')))
                         if '-' in item else [float(item), float(item)]
                         for item in borders]
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
        final_borders = list(filter(lambda x: x[0] <= x[1], merged_interval))
        final_borders.sort(key=lambda x: x[0])  # 排序
        if method:
            return self.equivalent(final_borders)
        else:
            return self.border(final_borders)

    # 根据给出的范围确定边界值
    @staticmethod
    def border(borders: list):
        boundary_values = []
        for start, end in borders:
            if start != end:
                start_left = [start - 0.1 ** (PublicUtil.count_decimal_places(start) + 1), False]
                start_right = [start + 0.1 ** (PublicUtil.count_decimal_places(start) + 1), True]
                end_left = [end - 0.1 ** (PublicUtil.count_decimal_places(start) + 1), True]
                end_right = [end + 0.1 ** (PublicUtil.count_decimal_places(start) + 1), False]
                middle = [(start + end)/2, True]
                boundary_values.extend([start_left, [start, True], start_right,
                                        middle, end_left, [end, True], end_right])
            else:
                boundary_values.append([start, True])
        print('已确认范围' + str(borders))
        print('已确认边界值' + str(boundary_values))

    # 根据给出的范围确定等价类
    @staticmethod
    def equivalent(borders: list):
        # total = input('请输入总范围（例如1-100），如果输入0则认为无限大范围').split('-')
        left = borders[0][0]
        right = borders[len(borders)-1][1]
        # equivalence_classes = [[f'小于{left}', False]] if len(total) == 0 else [[f'{total}']]
        equivalence_classes = [[f'小于{left}', False]]
        for index in range(len(borders)):
            if borders[index][0] != borders[index][1]:
                equivalence_classes.append([f'{borders[index][0]}-{borders[index][1]}', True])
            else:
                equivalence_classes.append([f'{borders[index][0]}', True])
            if index < len(borders) - 1:
                equivalence_classes.append([f'{borders[index][1]}-{borders[index+1][0]}', False])
        equivalence_classes.append([f'大于{right}', False])
        print('已确认范围' + str(borders))
        print('已确认等价类' + str(equivalence_classes))
        return equivalence_classes


