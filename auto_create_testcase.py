import json
from Dict.dicts import Dicts
from Util.utils import DataUtil, SelectUtil, PublicUtil


def main():
    api_url = input("请输入Restful API url")
    api_name = input("请输入接口对象名称")
    Dicts.API['url'] = api_url
    Dicts.API['name'] = api_name
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
            choose = int(input('————\n1-选择需要参数\n2-删除已选参数\n3-选择methods\n'))
            if choose == 1:
                selections = SelectUtil.select_params(all_keys, selections)
            elif choose == 2:
                selections = SelectUtil.del_params(selections)
            elif choose == 3:
                selections = SelectUtil.select_method(selections)
            else:
                break
    except json.JSONDecodeError as e:
        print("JSON 解析错误:", e)


if __name__ == "__main__":
    main()
