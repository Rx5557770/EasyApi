import json
import uuid

# 根据传入的api_id选择运行的脚本
# 函数内必须return code==200才扣除点数，否则失败不扣除。

def runfunc(api_id):
    if api_id == 1:
        res = dosomething()
    if api_id == 2:
        res = dosomething2()

    return res

def dosomething():
    data = {
        'code': 200,
        'data':'abcd',
        'info':'调试成功'
    }
    return data

def dosomething2():
    data = {
        'code': 500,
        'data':'abcd',
        'info':'调试失败'
    }
    return data
