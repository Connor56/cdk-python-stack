from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    CfnOutput,
)
from constructs import Construct


class FunctionStack(Stack):
    """
    Parameterisable CDK stack used to produce a single Lambda.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        handler: str,
        target_function_arn: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        fn = _lambda.Function(
            self,
            "Fn",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset("lambda"),
            handler=handler,
        )

        # Expose the function
        self.fn = fn

        url = fn.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,
            cors=_lambda.FunctionUrlCorsOptions(
                allowed_origins=["*"],
                allowed_methods=[_lambda.HttpMethod.ALL],
                allowed_headers=["*"],
            ),
        )

        # Add permission to invoke the target function if one is provided
        if target_function_arn is not None:
            fn.add_to_role_policy(
                iam.PolicyStatement(
                    actions=["lambda:InvokeFunction"],
                    resources=[target_function_arn],
                )
            )

            # Add environment variable for the target function ARN
            fn.add_environment("PEER_FN_ARN", target_function_arn)

        CfnOutput(
            self,
            "Url",
            value=url.url,
            description=f"URL for {id}",
        )
