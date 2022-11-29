import ujson as json
import boto3

BUCKET_NAME = "s3-sha-crackstation"
SHA_FILE_KEY = "data.json"

def lambda_handler(event, context):
    
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
        s3_client = boto3.client("s3")
        
        s3_select = s3_client.select_object_content(
            Bucket = BUCKET_NAME,
            Key = SHA_FILE_KEY,
            Expression = f"SELECT * FROM S3Object[*].sha[*] AS sha WHERE sha.ciphertext='{para}'",
            ExpressionType = 'SQL',
            InputSerialization = {"JSON": {"Type": "DOCUMENT"}},
            OutputSerialization = {"JSON": {"RecordDelimiter": ","}}
        )
        
        for evnt in s3_select["Payload"]:
            if "Records" in evnt:
                records = evnt["Records"]["Payload"].decode("utf-8")
                records = json.loads(records[:-1])
                
                return {
                    'statusCode': 200,
                    'body': json.dumps(
                        { para: records["plaintext"] }
                    )
                }
            else:
                return {
                    "statusCode": 404,
                    "body": json.dumps(
                        {
                            "message": "Non-crackable."
                        }
                    )
                }