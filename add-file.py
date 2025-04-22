import boto3
import json
import uuid 

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Inventory")

def lambda_handler(event, context):
    try:
        data = json.loads(event["body"])

        # Validate required fields
        required_fields = ["item_location_id", "name", "quantity"]
        for field in required_fields:
            if field not in data:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": f"Missing required field: {field}"})
                }

        item_id = str(uuid.uuid4())  # Generate a unique ID

        # Convert item_location_id and quantity to numbers
        item_location_id = int(data["item_location_id"])  
        quantity = int(data["quantity"])

        table.put_item(Item={
            "item_id": item_id,
            "item_location_id": item_location_id,  # Now stored as a number
            "name": data["name"],
            "quantity": quantity  # Ensure quantity is also stored as a number
        })

        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Item added successfully", "item_id": item_id})
        }

    except ValueError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid data type for item_location_id or quantity. Expected numbers."})
        }
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON format in request body"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

