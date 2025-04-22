import aws_cdk as cdk

from my_first_python_stack.my_first_python_stack_stack import FunctionStack

app = cdk.App()

function_2 = FunctionStack(
    app,
    "MyFunction2Stack",
    handler="lambda_function_2.lambda_handler",
)

FunctionStack(
    app,
    "MyFunctionStack",
    handler="lambda_function.lambda_handler",
    target_function_arn=function_2.fn.function_arn,
)

app.synth()
