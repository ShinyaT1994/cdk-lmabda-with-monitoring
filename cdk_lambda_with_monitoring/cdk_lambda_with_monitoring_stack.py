import os

from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
)
from constructs import Construct

from cdk_lambda_with_monitoring.lambda_with_monitoring import LambdaWithMonitoring


class CdkLambdaWithMonitoringStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # SNS Topic for notification
        operation_topic = sns.Topic(self, 'OperationTopic')
        subscription = operation_topic.add_subscription(
            subscriptions.EmailSubscription('shinya_takaramoto@ulvac.com')
        )
        
        # lambdaのLogGroupのError通知を成形しSNS Topicに渡す関数
        publish_message_function = lambda_.Function(
            self,
            'PublishMessageFunction',
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler='lambda_function.lambda_handler',
            code=lambda_.Code.from_asset(
                os.path.join('lambda', 'publish_message_function')
            ),
            environment={
                'OPERATION_TOPIC_ARN': operation_topic.topic_arn
            },
        )
        operation_topic.grant_publish(publish_message_function)
        
        # First lambda function with monitoring
        function_props_1 = {
            'code': lambda_.Code.from_asset(os.path.join('lambda', 'func1')),
            'handler': 'lambda_function.lambda_handler',
            'runtime': lambda_.Runtime.PYTHON_3_9,
            'function_name': 'test-lambda-func1',
            'memory_size': 128,
            'timeout': Duration.seconds(3)
        }
        
        lambda_with_monitoring_1 = LambdaWithMonitoring(
            self, 'LambdaWithMonitoring1', function_props_1, operation_topic,
            publish_message_function
        )
        
        # Second lambda function with monitoring
        function_props_2 = {
            'code': lambda_.Code.from_asset(os.path.join('lambda', 'func2')),
            'handler': 'lambda_function.lambda_handler',
            'runtime': lambda_.Runtime.PYTHON_3_8,
            'function_name': 'test-lambda-func2',
            'memory_size': 128,
            'timeout': Duration.seconds(10)
        }
        
        lambda_with_monitoring_2 = LambdaWithMonitoring(
            self, 'LambdaWithMonitoring2', function_props_2, operation_topic,
            publish_message_function
        )
