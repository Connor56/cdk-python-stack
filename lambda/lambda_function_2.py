import json
from typing import Dict, Any


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler

    :param event: dict, the event data sent by the requester
    :param context: LambdaContext, runtime information
    :return: dict,
    """

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Hello, this is Lambda 2!"}),
    }
