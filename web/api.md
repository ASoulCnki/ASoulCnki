# 枝网查重系统API 文档(version 1.0)

## 获取查重结果
### 简要描述
- 获取查重结果
### 请求URL
- `/v1/api/check`
### 请求方式
- POST
### 请求内容
- json
```json
{
    "text":"待查重文本"
}
```
### 返回内容
- json  
- 参数:  

|  参数名 | 类型  |  说明  |
|  ----  | ----  | ----  |
| code  | int | 状态码 |
| message  | string | 失败原因  |
| data  | json |  查重结果 |

- code:

|  code | 说明  |
|  ----  | ----  |
| 0  | 成功 |
| 4003 | 服务器内部错误 |

- data参数:

|  参数名 | 类型  |  说明  |
|  ----  | ----  | ----  |
| rate  | float | 重复率 |
| start_time  | int | 评论库开始时间戳|
| end_time  | int |  评论库结束时间戳 |
| related | list | 相似小作文 |

- related参数:  

|  参数名 | 类型  |  说明  |
|  ----  | ----  | ----  |
| text  | string | 小作文内容 |
| author  | string | 作者id |
| rate  | float | 与本篇文章的重复率 |

- 返回示例
```json
{
    "code":0,
    "message":"",
    "data":{
        "rate":0.1145141919780,
        "start_time":1624237336,
        "end_time":1624238336,
        "related":
        [
            {
                "text":"然然带我走吧",
                "author":"嘉然今天吃什么",
                "rate":"0.1145141919780"
            },
            {
                "text":"拉姐,带我走吧😭😭",
                "author":"蒙古上单",
                "rate":"0.10667"
            }
        ]
    }
}
```
```json
{
    "code":4003,
    "message":"服务器繁忙，请稍后再试",
    "data":{}
}
```

