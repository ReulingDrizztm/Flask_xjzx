from qiniu import Auth, put_data


def upload(f1):
    # 注册后的账号信息
    access_key = 'G'
    secret_key = 'W'
    # 空间名称
    bucket_name = 'python'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 生成上传 Token
    token = q.upload_token(bucket_name)
    # 上传文件数据，ret是字典，键为hash、key，值为新文件名，info是response对象
    ret, info = put_data(token, None, f1.read())
    # 返回文件名
    return ret.get('key')
