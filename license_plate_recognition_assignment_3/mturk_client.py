import boto3

MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

mturk = boto3.client('mturk',
                     region_name='us-east-1',
                     endpoint_url=MTURK_SANDBOX
                     )


def create_hit(bucket, key, flag):
    if not flag:
        hit_layout_id = '30QQN7XMMGNUT9IZDKHJOJ1FMQJ9H1'
    else:
        hit_layout_id = '30BL045PSP5M0UMGPCHE4YZPXYHCB5'
    value = f"https://{bucket}.s3.amazonaws.com/{key}"
    print(value)
    new_hit = mturk.create_hit(
        Title = "Does this car have 2 images",
        Description = "test",
        Reward='0.15',
        LifetimeInSeconds=72000,
        AssignmentDurationInSeconds=3600,
        MaxAssignments=1,
        HITLayoutId=hit_layout_id,
        HITLayoutParameters=[{'Name': 'image_url', 'Value': value}]
    )
    print("https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])
    print(new_hit)
    return new_hit


def get_initial_status(hit_id):
    print(mturk.list_assignments_for_hit(HITId=hit_id))


print(mturk.list_reviewable_hits())
get_initial_status('3T8DUCXY0PU2HNWP8JD3JE65IGH9TY')
