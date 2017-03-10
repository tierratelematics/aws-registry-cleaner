import boto3
import logging
import json
import datetime

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_untagged_images_older_than(ecr, repo_name, days):
    untagged_images = []

    filters = {
        'tagStatus': 'UNTAGGED'
    }

    images = ecr.describe_images(repositoryName=repo_name,filter=filters)["imageDetails"]
    for img in images:
        pushed_time = img["imagePushedAt"]
        time_threshold = datetime.date.today() - datetime.timedelta(days=int(days))
        if pushed_time.date() < time_threshold:
            untagged_images.append(img)
    return untagged_images

def clean_registry(days):
    ecr = boto3.client('ecr')
    repositories = ecr.describe_repositories()["repositories"]
    images_deleted = 0
    for repo in repositories:
        repo_name = repo["repositoryName"]
        untagged_images = get_untagged_images_older_than(ecr, repo_name, days)
        for img in untagged_images:
            ecr.batch_delete_image(
                registryId=img['registryId'],
                repositoryName=img['repositoryName'],
                imageIds=[
                {
                    'imageDigest': img['imageDigest']
                }
                ]
            )
            images_deleted += 1
    print("Deleted images: " + str(images_deleted))


def lambda_handler(event, context):

     clean_registry(event["days"])
