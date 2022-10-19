import boto3


class Config:
    DB_REGION_NAME = "eu-west-1"
    DB_ACCESS_KEY_ID = "lolkek"
    DB_SECRET_ACCESS_KEY = "lolkek"


ddb = boto3.resource('dynamodb',
                     endpoint_url="http://dynamodb-local:8001",
                     region_name=Config.DB_REGION_NAME,
                     aws_access_key_id=Config.DB_ACCESS_KEY_ID,
                     aws_secret_access_key=Config.DB_SECRET_ACCESS_KEY)
try:
    ddb.create_table(TableName="Statistics",
                     AttributeDefinitions=[
                         {
                             "AttributeName": "page_id",
                             "AttributeType": "N"
                         }
                     ],
                     KeySchema=[
                         {
                             "AttributeName": "page_id",
                             "KeyType": "HASH"
                         }
                     ]
                     ,
                     ProvisionedThroughput=
                     {
                         "ReadCapacityUnits": 10,
                         "WriteCapacityUnits": 5
                     }
                     )
except Exception as e:
    if e.__class__.__name__ == 'ResourceInUseException':
        pass
    else:
        raise e

table = ddb.Table("Statistics")
