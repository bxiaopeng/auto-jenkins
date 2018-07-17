# auto-jenkins

## 连接

### 连接job

### 连接Jenkins



## 构建

### 获取构建任务所需参数的信息

代码：

```python
params_defines = server.get_job_info("job_name").build_params.defines
ppirnt.pprint(params_defines)
```

输出:

```json
[{'default_value': 'test',
  'description': '',
  'name': 'env',
  'type': 'choices',
  'values': ['test', 'online', 'release', 'uat']},
 {'default_value': 'all',
  'description': '',
  'name': 'plevel',
  'type': 'choices',
  'values': ['all', 'p1', 'p2', 'p3']},
 {'default_value': '"wlqd,invoie,printExpress,filter,addressConfirm"',
  'description': '',
  'name': 'groups',
  'type': 'checkbox',
  'values': ''}]
```

说明：

name: 参数名

description: 参数的描述

type: 参数的类型

default_value: 默认值，传参类型可参考此值

values: 参数的可选值



### 获取构建任务的默认参数

```python
default_parameter_values = server.get_job_info("job-name").build_params.default_parameter_values
```

为空则返回 None

### 构建任务

```python
server.build_job("job_name",parameters)
```



