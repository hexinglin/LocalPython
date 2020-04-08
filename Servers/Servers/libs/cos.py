# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 bucketname-appid 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = 'AKIDNYGURGQ78sCFdnvJe5FH3YmjSWMvGlLe'      # 替换为用户的 secretId
secret_key = 'AUXJo3GaieSzFJC2YtwrWtzpfJkuwh02'      # 替换为用户的 secretKey
region = 'ap-chengdu'      # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)

# response = client.upload_file(
#     Bucket='stock-1252668295',
#     # LocalFilePath=settings.BASE_DIR + '/static/Result1.csv',
#     Key='Result1',
#     PartSize=10,
#     MAXThread=10
# )
# print(response)








