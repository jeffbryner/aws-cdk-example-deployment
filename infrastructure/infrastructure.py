from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
    aws_ecs_patterns as ecs_patterns,
)
from aws_cdk.aws_elasticloadbalancingv2 import ApplicationProtocol
from aws_cdk.aws_ecr_assets import DockerImageAsset


class SampleTwoServiceStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        vpc = ec2.Vpc(self, "SampleVPC", max_azs=2)  # default is all AZs in region
        cluster = ecs.Cluster(self, "ServiceCluster", vpc=vpc)
        cluster.add_default_cloud_map_namespace(name="service.local")

        # two docker containers
        # two ECS services/tasks

        frontend_asset = DockerImageAsset(
            self, "frontend", directory="./frontend", file="Dockerfile"
        )
        frontend_task = ecs.FargateTaskDefinition(
            self, "frontend-task", cpu=512, memory_limit_mib=2048,
        )
        frontend_task.add_container(
            "frontend",
            image=ecs.ContainerImage.from_docker_image_asset(frontend_asset),
            essential=True,
            environment={"LOCALDOMAIN": "service.local"},
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="FrontendContainer",
                log_retention=logs.RetentionDays.ONE_WEEK,
            ),
        ).add_port_mappings(ecs.PortMapping(container_port=5000, host_port=5000))

        backend_task = ecs.FargateTaskDefinition(
            self, "backend-task", cpu=512, memory_limit_mib=2048,
        )
        backend_task.add_container(
            "backend",
            image=ecs.ContainerImage.from_registry("redis:alpine"),
            essential=True,
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="BackendContainer",
                log_retention=logs.RetentionDays.ONE_WEEK,
            ),
        ).add_port_mappings(ecs.PortMapping(container_port=6379, host_port=6379))

        frontend_service = ecs_patterns.NetworkLoadBalancedFargateService(
            self,
            id="frontend-service",
            service_name="frontend",
            cluster=cluster,  # Required
            cloud_map_options=ecs.CloudMapOptions(name="frontend"),
            cpu=512,  # Default is 256
            desired_count=2,  # Default is 1
            task_definition=frontend_task,
            memory_limit_mib=2048,  # Default is 512
            listener_port=80,
            public_load_balancer=True,
        )

        frontend_service.service.connections.allow_from_any_ipv4(
            ec2.Port.tcp(5000), "flask inbound"
        )

        backend_service = ecs_patterns.NetworkLoadBalancedFargateService(
            self,
            id="backend-service",
            service_name="backend",
            cluster=cluster,  # Required
            cloud_map_options=ecs.CloudMapOptions(name="backend"),
            cpu=512,  # Default is 256
            desired_count=2,  # Default is 1
            task_definition=backend_task,
            memory_limit_mib=2048,  # Default is 512
            listener_port=6379,
            public_load_balancer=False,
        )

        backend_service.service.connections.allow_from(
            frontend_service.service, ec2.Port.tcp(6379)
        )
