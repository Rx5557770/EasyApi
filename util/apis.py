
# 根据传入的api_id选择运行的脚本
# 函数内必须return code==200才扣除点数，否则失败不扣除。
def runfunc(api_id, params):
    # 接口id: 方法
    api_config = {
        1: dosomething,
        2: dosomething2,
        3: dosomething3,
    }

    res = api_config[api_id](params)
    return res

def dosomething(params=None):
    data = {
        'code': 200,
        'data':'abcd',
        'msg':'调试成功'
    }
    return data

def dosomething2(params):
    data = {
        'code': 200,
        'data':'abcd',
        'msg':'调试成功',
        'params':params
    }
    return data


def dosomething3(params=None):
    data = {
        'code': 501,
        'data':'abcd',
        'msg':'调试失败'
    }
    return data

