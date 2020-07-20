# aws-cdk-example-deployment
A working example of using aws cdk to deploy multiple docker containers


## to make it go

```bash

git clone https://github.com/jeffbryner/aws-cdk-example-deployment.git
cd aws-cdk-example-deployment
npm install -g aws-cdk
pipenv --python 3.8
pipenv shell
pipenv install aws-cdk.core aws-cdk.cx-api aws-cdk.cloud-assembly-schema
pipenv install aws_cdk.aws_ec2 aws_cdk.aws_ecs aws_cdk.aws_ecs_patterns
cdk synth
```