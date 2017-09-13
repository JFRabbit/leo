# leo
Python interface test(compare JSON &amp; HTTP requeset)

## Prepare json data.

Set a dict object to create CompareData:

```
expect = dict{...}
actual = dict{...}

e_data = CompareData(200, expect, True) # http code, dict, isExpect
a_data = CompareData(200, actual, False)

print(e_data)
print(a_data)
```

## How to create Comparator?


```
comparator = Comparator()
```


## Compare


```
result = comparator.compare(e_data, a_data)
print(result)
```

Example:

```
====================
IsSame:
	False
ErrorMsg:
	errorPath:	-root-obj-array[result][0]-obj[2][status]
	errorCode:	VALUE_DIFF
	errorMsg:
		Expect: 0
		Actual: 1
	====================
```



## How to set compare rule?

The defualt path is "PATH_ROOT"(compareConstant.py, PATH_ROOT).

If some object have no key name, for exapmle: 


```
"result":   [
                {
                    "code": "EXTRACTION", 
                    "type": "ANALYSIS", 
                    "status": 1, 
                    "name": "192.168.0.1"
                }, ...
            ]
```

use key: "result:subObj"(compareConstant.py, SUB_OBJ)

Rule detail:

    
```
IS_ANY_INTEGER = "${IS_ANY_INTEGER}"
IS_ANY_FLOAT = "${IS_ANY_FLOAT}"
IS_ANY_STRING = "${IS_ANY_STRING}"
IS_TIMESTEMP = "${IS_TIMESTEMP}"  # '%Y-%m-%d %H:%M:%S'

MATCH_REGEX = "${MATCH_REGEX}"

IGNORE_VALUE = "${IGNORE_VALUE}"
IGNORE_OBJECT_KEY_MISS_MATCH = "${IGNORE_OBJECT_KEY_MISS_MATCH}"
IGNORE_ARRAY_SIZE = "${IGNORE_ARRAY_SIZE}"

IS_JSON_OBJECT = "${IS_JSON_OBJECT}"
IS_JSON_ARRAY = "${IS_JSON_ARRAY}"
IS_JSON_PRIMITIVE = "${IS_JSON_PRIMITIVE}"
```

    
You can set rules ues "set_rule":


```
comparator.set_rule(PATH_ROOT, Rule.IGNORE_OBJECT_KEY_MISS_MATCH)
comparator.set_rule("result", Rule.IGNORE_ARRAY_SIZE)
comparator.set_rule("result" + SUB_OBJ, Rule.IGNORE_OBJECT_KEY_MISS_MATCH)
```

    
Or set dict expect data:

    
```
expect =    {
                "code": "${IS_ANY_INTEGER}", 
    	    	"message": "${IS_ANY_STRING}",
                "result": [
                        {
                            "code1": "${IS_JSON_PRIMITIVE}", 
                        	"type": "ANALYSIS", 
                        	"status": 0, 
                        	"name": "${MATCH_REGEX}(([01]?\d?\d|2[0-4]\d|25[0-5])\.){3}([01]?\d?\d|2[0-4]\d|25[0-5]\.)"},
                		
                        {
                            "code": "PREPROCESSING", 
                            "type": "ANALYSIS", 
                            "status": 1, 
                            "name": "数据预处理", 
                            "foo": "bar"},
                		     
                        {
                            "code": "TRAINING", 
                            "type": "${IGNORE_VALUE}", 
                            "status": "${IS_ANY_FLOAT}", 
                            "name": "模型训练"},
                		     
                        {
                            "code": "SCORING", 
                            "type": "ANALYSIS", 
                            "status": 0, 
                            "name": "${IS_TIMESTEMP}"}]
            }
```

