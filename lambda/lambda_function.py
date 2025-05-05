import json
from typing import Dict, Any
import boto3
import os
import numpy as np

# Set up the client to communicate with AWS and the other Lambda function
client = boto3.client("lambda")
ssm = boto3.client("ssm")


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler

    :param event: dict, the event data sent by the requester
    :param context: LambdaContext, runtime information
    :return: dict,
    """

    body = json.loads(event["body"])

    # Standard Response
    if "calledBy" in body:
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": f"Hello, {body['calledBy']}!"}),
        }

    # Call secondary Lambda function to get response
    response = client.invoke(
        FunctionName=os.environ["PEER_FN_ARN"],
        InvocationType="RequestResponse",
        Payload=json.dumps(
            {
                "calledBy": "MyFunction",
            }
        ),
    )

    # Parse secondary Lambda function's response
    result = json.loads(response["Payload"].read())

    numpy_array = np.array([1, 2, 3])
    dot_product = numpy_array @ numpy_array

    result["numpy_array"] = numpy_array.tolist()
    result["dot_product"] = int(dot_product)

    some_random_key = ssm.get_parameter(Name="SomeRandomKey")

    result["some_random_key"] = some_random_key["Parameter"]["Value"]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result),
    }
