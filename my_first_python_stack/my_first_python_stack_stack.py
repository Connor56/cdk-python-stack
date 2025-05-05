from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_ssm as ssm,
    aws_iam as iam,
    CfnOutput,
    BundlingOptions,
)
from constructs import Construct
import os
from dotenv import load_dotenv

load_dotenv("../.env")


class MyFirstPythonStackStack(Stack):
    """
    Two Lambda functions and dedicated URLS. One function with
    permission to invoke the other.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a function
        fn = _lambda.Function(
            self,
            "MyFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset(
                "lambda",
                bundling=BundlingOptions(
                    image=_lambda.Runtime.PYTHON_3_11.bundling_image,
                    command=[
                        "bash",
                        "-c",
                        # install into /asset-output and copy your code
                        "pip install -r requirements.txt -t /asset-output && "
                        "cp -ru . /asset-output",
                    ],
                ),
            ),
            handler="lambda_function.lambda_handler",
        )

        fn_url = fn.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,
            cors=_lambda.FunctionUrlCorsOptions(
                allowed_origins=["*"],
                allowed_methods=[_lambda.HttpMethod.ALL],
                allowed_headers=["*"],
            ),
        )

        # Create a parameter store secret
        secret = ssm.StringParameter(
            self,
            id="SomeRandomKey",
            parameter_name="SomeRandomKey",
            description="A random key to test",
            string_value=os.getenv("SomeRandomKey"),
        )

        # Grent read access to the first function
        secret.grant_read(fn)

        # Create a function
        fn2 = _lambda.Function(
            self,
            "MyFunction2",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset("lambda"),
            handler="lambda_function_2.lambda_handler",
        )

        fn_url2 = fn2.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,
            cors=_lambda.FunctionUrlCorsOptions(
                allowed_origins=["*"],
                allowed_methods=[_lambda.HttpMethod.ALL],
                allowed_headers=["*"],
            ),
        )

        # Grant fn permission to invoke fn2
        fn.add_to_role_policy(
            iam.PolicyStatement(
                actions=["lambda:InvokeFunction"],
                resources=[fn2.function_arn],
            )
        )
        # This can also be done with
        # fn.grant_invoke(fn2)

        # Expose the second function's ARN to the first function
        fn.add_environment("PEER_FN_ARN", fn2.function_arn)

        CfnOutput(
            self,
            "MyFunctionUrl",
            value=fn_url.url,
            description=f"URL for the MyFunction Lambda function",
        )

        CfnOutput(
            self,
            "MyFunction2Url",
            value=fn_url2.url,
            description=f"URL for the MyFunction2 Lambda function",
        )
