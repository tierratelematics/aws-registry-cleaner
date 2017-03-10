#!/usr/bin/python
import boto3
import zipfile
import json

aws=boto3.Session(region_name=('eu-west-1'))
lam=aws.client('lambda')
cwe=aws.client('events')

zf = zipfile.ZipFile('lamba-script-package.zip', mode='w')
try:
    zf.write('registry-cleaner.py')
finally:
    zf.close()

rule_name = "docker-registry-cleaner"
# Clean previous items
try:
    lam.delete_function(
        FunctionName=rule_name
        )
    cwe.remove_targets(
        Rule=rule_name,
        Ids=[ rule_name ]
    )
    cwe.delete_rule(
        Name=rule_name
    )
except:
    pass

# Create Rule
rule = cwe.put_rule(
    Name=rule_name,
    ScheduleExpression="rate(1 day)"
    )

lf = lam.create_function(FunctionName=rule_name,
                         Runtime='python2.7',
                         Role='arn:aws:iam::345762685377:role/lambda_ecr_cleaner',
                         Handler='registry-cleaner.lambda_handler',
                         Code={
                            'ZipFile': open('lamba-script-package.zip', 'rb').read(),
                         },
                         Timeout=15,
                         MemorySize=128)

lam.add_permission(FunctionName=rule_name,
                   StatementId=rule_name,
                   Action='lambda:InvokeFunction',
                   Principal='events.amazonaws.com',
                   SourceArn=rule["RuleArn"])

lf_input = {
        'days': 60
    }

cwe.put_targets(Rule=rule_name,
                Targets=[{'Id': rule_name,
                            'Arn': lf['FunctionArn'],
                            'Input': json.dumps(lf_input)}])
