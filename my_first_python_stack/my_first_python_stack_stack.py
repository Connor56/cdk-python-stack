from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
)
from constructs import Construct


class MyFirstPythonStackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Base lambda function set up
        fn = _lambda.Function(
            self,
            "MyFunction",  # The name of the function in Cloud Formation
            runtime=_lambda.Runtime.PYTHON_3_11,  # You runtime environment
            code=_lambda.Code.from_asset("lambda"),  # Your code directory
            handler="lambda_function.lambda_handler",  # Your <module>.<handler-function>
        )

        # Create a function URL for the Lambda function
        fn_url = fn.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,  # Public access, no Auth required
            cors=_lambda.FunctionUrlCorsOptions(
                allowed_origins=[
                    "*"
                ],  # Allow the request to come from any origin
                allowed_methods=[
                    _lambda.HttpMethod.ALL
                ],  # Allow the request to have any http method
                allowed_headers=["*"],  # Allow any headers in the request
            ),
        )

        # Output the function URL
        from aws_cdk import CfnOutput

        # Print the URL address to the terminal when you deploy
        CfnOutput(
            self,
            "FunctionUrl",
            value=fn_url.url,
            description="URL for the Lambda function",
        )
