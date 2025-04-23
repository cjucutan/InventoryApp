import boto3
import json
 
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')
INDEX_NAME = 'GSI_Reverse_PK_SK'  # make sure this exists
 
def lambda_handler(event, context):
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }
 
    id = event['pathParameters']['id']
 
    try:
        # Query the GSI to get the item_location_id
        response = table.query(
            IndexName=INDEX_NAME,
            KeyConditionExpression=boto3.dynamodb.conditions.Key('id').eq(id)
        )
 
        items = response.get('Items', [])
        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps("Item not found")
            }
 
        # Assume item_id is unique, use the first match
        item = items[0]
        location_id = item['item_location_id']
 
        # Perform the delete
        table.delete_item(
            Key={
                'id': id,
                'location_id': location_id
            }
        )
 
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item {id} deleted successfully.")
        }
 
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
