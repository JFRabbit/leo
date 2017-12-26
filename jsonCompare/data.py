# coding=utf-8
expect = {"code": "${IS_ANY_INTEGER}", "message": "${IS_ANY_STRING}",
          "result": [{"code1": "${IS_JSON_PRIMITIVE}", "type": "ANALYSIS", "status": 0, "name": "${MATCH_REGEX}(([01]?\d?\d|2[0-4]\d|25[0-5])\.){3}([01]?\d?\d|2[0-4]\d|25[0-5]\.)"},
                     {"code": "PREPROCESSING", "type": "ANALYSIS", "status": 1, "name": "数据预处理", "foo": "bar"},
                     {"code": "TRAINING", "type": "${IGNORE_VALUE}", "status": "${IS_ANY_FLOAT}", "name": "模型训练"},
                     {"code": "SCORING", "type": "ANALYSIS", "status": 0, "name": "${IS_TIMESTEMP}"}]}

actual = {"code": 0, "message": "111",
          "result": [{"code": "EXTRACTION", "type": "ANALYSIS", "status": 1, "name": "192.168.0.1"},
                     {"code": "PREPROCESSING", "type": "ANALYSIS", "status": 1, "name": "数据预处理"},
                     {"code": "TRAINING", "type": "ANALYSIS", "status": 1.01, "name": "模型训练"},
                     {"code": "SCORING", "type": "ANALYSIS", "status": 0, "name": "1990-09-11 11:28:30"},
                     {"code": "SCORING", "type": "ANALYSIS", "status": 0, "name": "1990-09-11 11:28:30"}],
          "foo":"bar"}

if __name__ == '__main__':
    print(expect)

    import json
    r = json.dumps(expect,  sort_keys=True, indent=4, ensure_ascii=False)
    print(r)