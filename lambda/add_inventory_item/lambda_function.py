import json
import boto3
import uuid

def lambda_handler(event, context):
    try:
        data = json.loads(event[ 'body'])
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide some data")
        }
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Inventory')

    unique_id = str(uuid.uuid4())

    try:
        table.put_item(
            Item={
                'id': unique_id,
                'name': data['name'],
                'Description': data['Description'],
                'qty': int(data['qty']),
                'price': str(data['price']),
                'location_id': int(data['location_id'])
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {unique_id} added successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }
