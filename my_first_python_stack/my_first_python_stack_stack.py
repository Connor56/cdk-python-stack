from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    CfnOutput,
)
from constructs import Construct


class MyFirstPythonStackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        functions = [
            {
                "id": "MyFunction",
                "handler": "lambda_function.lambda_handler",
            },
            {
                "id": "MyFunction2",
                "handler": "lambda_function_2.lambda_handler",
            },
        ]

        for cfg in functions:
            fn = _lambda.Function(
                self,
                cfg["id"],
                runtime=_lambda.Runtime.PYTHON_3_11,
                code=_lambda.Code.from_asset("lambda"),
                handler=cfg["handler"],
            )

            fn_url = fn.add_function_url(
                auth_type=_lambda.FunctionUrlAuthType.NONE,
                cors=_lambda.FunctionUrlCorsOptions(
                    allowed_origins=["*"],
                    allowed_methods=[_lambda.HttpMethod.ALL],
                    allowed_headers=["*"],
                ),
            )

            CfnOutput(
                self,
                f"{cfg['id']}Url",
                value=fn_url.url,
                description=f"URL for the {cfg['id']} Lambda function",
            )
