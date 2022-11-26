import ujson as json
import boto3

def lambda_handler(event, context):
    
    BUCKET_NAME = "s3-sha-crackstation"
    SHA1_FILE_KEY = "sha1-data.json"
    SHA2_FILE_KEY = "sha2-data.json"
    
    try:
        para = event["pathParameters"]["shaHash"]
    except:
        return {
            "statusCode": 400,
            "body": json.dumps(
                { "message": "Path parameters `/{shaHash}` not found." }
            )
        }
    
    if len(para) not in [40, 64]:
        return {
            "statusCode": 404,
            "body": json.dumps(
                {
                    "message": "Non-crackable."
                }
            )
        }
    else:
        s3 = boto3.resource("s3")
        if len(para) == 40:
            s3.Bucket(BUCKET_NAME).download_file(SHA1_FILE_KEY, f"/tmp/data.json")
        else:
            s3.Bucket(BUCKET_NAME).download_file(SHA2_FILE_KEY, f"/tmp/data.json")
            
        with open("/tmp/data.json", "r") as json_file:
            data = json.loads(json_file.read())
        
        result = data.get(para)
        
        if result == None:
            return {
                "statusCode": 404,
                "body": json.dumps(
                    {
                        "message": "Non-crackable."
                    }
                )
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(
                    { para: result }
                )
            }