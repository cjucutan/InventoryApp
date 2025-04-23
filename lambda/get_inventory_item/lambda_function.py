import boto3
import json
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')
INDEX_NAME = 'ItemIdIndex'  # name of your GSI

def convert_decimals(obj):
   if isinstance(obj, list):
       return [convert_decimals(i) for i in obj]
   elif isinstance(obj, dict):
       return {k: convert_decimals(v) for k, v in obj.items()}
   elif isinstance(obj, Decimal):
       return int(obj) if obj % 1 == 0 else float(obj)
   return obj

def lambda_handler(event, context):
   if 'pathParameters' not in event or 'id' not in event['pathParameters']:
       return {
           'statusCode': 400,
           'body': json.dumps("Missing 'id' path parameter")
       }

   id = event['pathParameters']['id']

   try:
       # Query the GSI by id
       response = table.query(
           IndexName=INDEX_NAME,
           KeyConditionExpression=Key('id').eq(id)
       )
       items = response.get('Items', [])

       if not items:
           return {
               'statusCode': 404,
               'body': json.dumps('Item not found')
           }

       return {
           'statusCode': 200,
           'body': json.dumps(convert_decimals(items[0]))
       }

   except Exception as e:
       return {
           'statusCode': 500,
           'body': json.dumps(str(e))
       }
