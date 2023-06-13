import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_lambda_with_monitoring.cdk_lambda_with_monitoring_stack import CdkLambdaWithMonitoringStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_lambda_with_monitoring/cdk_lambda_with_monitoring_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkLambdaWithMonitoringStack(app, "cdk-lambda-with-monitoring")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
