import os

from aws_cdk import (
    Duration,
    Stack,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cloudwatch_actions,
    aws_lambda as lambda_,
    aws_logs as logs,
    aws_logs_destinations as logs_destinations,
)
from constructs import Construct


class LambdaWithMonitoring(Construct):
    def __init__(
            self, scope: Construct, construct_id: str, function_props, 
            operation_topic, publish_message_function, **kwargs) -> None:
        """
        Initialize method
        
        parameters
        ----------
        function_props: dict
            Lambda関数のプロパティ
        sns_topic: aws_sns.Topic
            Alarmの内容を通知するTopic
        publish_message_function: lambda.Function
            lambdaのLogGroupのError通知を成形しSNS Topicに渡す関数
        """
        super().__init__(scope, construct_id, **kwargs)
        
        # Create lambda function
        lambda_function = lambda_.Function(
            self, f'{construct_id}LambdaFunction', **function_props
        )
        
        # Throttle error alarm
        throttles_alarm = cloudwatch.Alarm(
            self, f'{construct_id}ThrottlesAlarm',
            metric=cloudwatch.Metric(
                metric_name='Throttles',
                namespace='AWS/Lambda',
                dimensions_map={'FunctionName': lambda_function.function_name},
                period=Duration.minutes(1),
                statistic='Sum',
            ),
            evaluation_periods=1,
            threshold=0,
            comparison_operator \
                =cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
        )
        throttles_alarm.add_alarm_action(
            cloudwatch_actions.SnsAction(operation_topic)
        )
        
        # LogGroup error alarm
        lambda_function.log_group.add_subscription_filter(
            f'{construct_id}SubscriptionFilter',
            destination=logs_destinations.LambdaDestination(
                publish_message_function
            ),
            filter_pattern=logs.FilterPattern.any_term('ERROR'),
        )