import os
import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

COMMON_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",  # helpful later with API Gateway
}

def resp(status: int, body) -> dict:
    return {"statusCode": status, "headers": COMMON_HEADERS, "body": json.dumps(body)}

def handler(event, context):
    """
    Supports REST-style calls via API Gateway (REST API):
      POST   /students                 -> create (body: {student_id, ...})
      GET    /students                 -> list (scan up to 50 items)
      GET    /students/{student_id}    -> read
      PUT    /students/{student_id}    -> update (body: fields to change)
      DELETE /students/{student_id}    -> delete
    """
    method = (event or {}).get("httpMethod", "")
    path_params = (event or {}).get("pathParameters") or {}
    student_id = path_params.get("student_id")
    body_str = (event or {}).get("body") or "{}"
    try:
        data = json.loads(body_str)
    except json.JSONDecodeError:
        return resp(400, {"error": "Request body must be valid JSON"})

    try:
        if method == "POST":
            # Create
            sid = str(data.get("student_id") or "").strip()
            if not sid:
                return resp(400, {"error": "student_id is required"})
            item = {
                "student_id": sid,
                "name": data.get("name"),
                "course": data.get("course"),
                "email": data.get("email"),
            }
            # remove nulls
            item = {k: v for k, v in item.items() if v is not None}
            table.put_item(Item=item)
            return resp(201, {"message": "Student record added", "item": item})

        elif method == "GET":
            if student_id:
                # Read single
                res = table.get_item(Key={"student_id": str(student_id)})
                item = res.get("Item")
                if not item:
                    return resp(404, {"error": "Not found"})
                return resp(200, item)
            else:
                # List (demo only)
                res = table.scan(Limit=50)
                return resp(200, res.get("Items", []))

        elif method == "PUT": #update function
            # Update (id in path OR body)
            sid = str(student_id or data.get("student_id") or "").strip()
            if not sid:
                return resp(400, {"error": "student_id is required"})
            update_fields = {k: v for k, v in data.items() if k != "student_id"}
            if not update_fields:
                return resp(400, {"error": "No fields to update"})
            update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in update_fields)
            expr_names = {f"#{k}": k for k in update_fields}
            expr_vals = {f":{k}": v for k, v in update_fields.items()}
            table.update_item(
                Key={"student_id": sid},
                UpdateExpression=update_expr,
                ExpressionAttributeNames=expr_names,
                ExpressionAttributeValues=expr_vals,
                ReturnValues="ALL_NEW",
            )
            res = table.get_item(Key={"student_id": sid})
            return resp(200, res.get("Item"))

        elif method == "DELETE": #delete function
            if not student_id:
                return resp(400, {"error": "student_id path parameter is required"})
            table.delete_item(Key={"student_id": str(student_id)})
            return resp(200, {"message": "Deleted"})

        else:
            return resp(405, {"error": f"Method {method} not allowed"})

    except Exception as e:
        # Log the error automatically via CloudWatch
        return resp(500, {"error": "Internal error", "detail": str(e)})
