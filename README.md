# AWS registry cleaner

This repo contains a script useful to clean docker images untagged from ECR repository older than n days. Moreover there is a Python Script that using boto3 library to create all lamba functions directly on AWS.

## Usage
Edit create-lambda-function.py and decide how many days you want keep untagged images.
```python
lf_input = {
        'days': 60
    }
```

Create a role for this lambda fuction with policy AmazonEC2ContainerRegistryPowerUser and put arn in the 
```python
lf = lam.create_function(FunctionName=rule_name,
                         Runtime='python2.7',
                         Role='arn:aws:iam::345762685377:role/lambda_ecr_cleaner',
```

Once you have edit, launch from shell create-lambda-function.py script.
The scheduler is once per day.

### Requirements
- python 2.7
- boto3 library
- aws command line configured with your credential
