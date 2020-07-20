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

# if you've not used cdk before you may need to bootstrap it into
# your aws environment (creates s3 bucket for cloud formation templates, etc)

cdk bootstrap

# test run to see if it creates a template
cdk synth

# if it's good, then deploy
cdk deploy

# it should warn you about upcoming changes and ask you to accept (a security precaution)
# at the end of the deployment you'll get outputs to the two loadbalanced services
# copy the url for the 'frontend' one, toss it into your browser and you should see the demo page

# clean up with a
cdk destroy
```