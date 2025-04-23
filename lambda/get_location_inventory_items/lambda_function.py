import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

TABLE_NAME = 'Inventory'
GSI_NAME = 'GSI_Reverse_PK_SK'

def lambda_handler(event, context):
    
    table = dynamodb.Table(TABLE_NAME)

    try:
        response = table.query(
            IndexName=GSI_NAME,
            KeyConditionExpression = Key('location_id').eq(324)
        )
        items = response.get('Items', [])

        def decimal_to_float(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            raise TypeError("Object of the type Decimal is not JSON serializable")
        
        items = json.loads(json.dumps(items, default = decimal_to_float))

    except ClientError as e:
        print(f"Failed to query items: {e.response['Error']['Message']}")
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to query items'})
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
