import aws_cdk as core
import aws_cdk.assertions as assertions

from my_first_python_stack.my_first_python_stack_stack import MyFirstPythonStackStack

# example tests. To run these tests, uncomment this file along with the example
# resource in my_first_python_stack/my_first_python_stack_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MyFirstPythonStackStack(app, "my-first-python-stack")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
