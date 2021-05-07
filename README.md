# 特殊msg

* SUCCESS 成功
* EXPIRED 会话超时

# 核心功能

## 查询证书 /querycert POST

### 参数 json

```json5
{
  "stu_id": ""
  // 学生身份证
}
```

---OR---

```json5
{
  "cert_id": "",
  //证书编号
  "stu_id": ""
}
```

此方式无需Session

### 返回 json

```json5
{
  "msg": "SUCCESS",
  // 成功即为SUCCESS, 不成功未错误提示内容 str
  "certs": [
    {
      "stu_name": "",
      //学生姓名 str
      "cert_id": "",
      //证书编号 str
      "school_name": "",
      //学校名称 str
      "degree": "",
      // 学位等级 str
      "edu_system": "",
      // 学制 str,
      "stu_major": "",
      // 专业 str 可选
    }
  ]
}
```

## 添加 /issuecert POST

### 参数 json

```json5
{
  "stu_id": "",
  //学生身份证号 str
  "stu_name": "",
  //学生姓名 str
  "cert_id": "",
  //证书编号 str
  "school_name": "",
  //学校名称 str
  "degree": "",
  // 学位等级 str
  "edu_system": "",
  // 学制 str,
  "stu_major": "",
  // 专业 str 可选
}
```

### 返回 json

```json5
{
  "msg": "SUCCESS"
}
```

## 修改 /modifycert POST

### 参数 json

同添加证书

### 返回 json

```json5
{
  "msg": "SUCCESS"
}
```

# 登录功能

## 登录 /login

### 参数 json

```json5
{
  "stu_id": "",
  // 学生的身份证号
  "pri_key_sum": "",
  // 学生私钥 hex-MD5
}
```

### 返回 json

```json5
{
  "msg": "SUCCESS",
  "level": 0,
  // 0-学生，1-管理员，2-全局管理员
}
```

### COOKIE设置

* session 在中间件暂存pri_key，并返回其对应的session号。之后所有的操作都需要验证Session有效性，并通过Session号获取对应的私钥

## 登出 /logout GET

### 参数

无，中间件应根据Cookie判断对应的Session

### 返回 json

```json5
{
  "msg": "SUCCESS"
  // 并clearCookie
}
```

## 验证 /verifyuser GET

### 参数

无，中间件应根据Cookie判断是否存在有效的Session

### 返回 json

```json5
{
  "msg": "SUCCESS",
  "id": "admin",
  "level": 2
  // 若无效则为 EXPIRED
}
```

# 杂项脚本

## 安装链码

### 脚本输入参数解释

* peer number 当前channel中节点数量
* cc name 链码的名字
* channel ID channel的ID
* cc version 链码的版本，建议从1.0开始
* cc sequence 链码的序列，每安装一次新链码序列加一，从1开始
* chaincode packed file 打包链码的文件名

### 注意事项

* 请放置于test-network目录运行
* 请提前打包好链码
* 默认了一些东西，详情见脚本