#!/usr/bin/env python3

from aws_cdk import core
from infrastructure.infrastructure import SampleTwoServiceStack

app = core.App()
ecs = SampleTwoServiceStack(app, "SampleStack")
app.synth()
