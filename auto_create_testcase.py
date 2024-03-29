import json
import logging
from Util.utils import PublicUtil, DataUtil, SelectUtil


def main():
    json_str = ""
    print("请输入JSON请求体并以空行结束")
    while True:
        line = input()
        if line:
            json_str += line
        else:
            break
    try:
        dict_data = json.loads(json_str)
        data_util = DataUtil()
        all_keys = data_util.get_all_keys(json_data=dict_data)
        selections = []
        while True:
            choose = int(input('1-选择需要参数\n2-删除已选参数\n'))
            if choose == 1:
                selections = SelectUtil.select_params(all_keys, selections)
            elif choose == 2:
                selections = SelectUtil.del_params(selections)
            else:
                break
    except json.JSONDecodeError as e:
        print("JSON 解析错误:", e)


if __name__ == "__main__":
    main()
