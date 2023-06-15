#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_lambda_with_monitoring.cdk_lambda_with_monitoring_stack import CdkLambdaWithMonitoringStack


app = cdk.App()
CdkLambdaWithMonitoringStack(app, "CdkLambdaWithMonitoringStack")

app.synth()
