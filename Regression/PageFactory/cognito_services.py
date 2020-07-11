"""cognito help"""
import boto3


def get_pool_id(pool_name):
    cognito = boto3.client('cognito-idp')
    pools = cognito.list_user_pools(
        MaxResults=59
    )
    # print([p for p in pools['UserPools']])

    try:
        pool = [
            p for p in pools['UserPools']
            if p['Name'] == pool_name
        ]
        # print("found pool", pool)

        return pool[0]['Id']
    except Exception as e:
        print("Failed to find pool", repr(e))
        raise


def get_user(pool_id, user_email):
    cognito = boto3.client('cognito-idp')
    users = cognito.list_users(
        UserPoolId=pool_id,
        AttributesToGet=['email'],
        # MaxResults=100,
        # HideDisabled=True,
    )
    # import pprint
    # pprint.pprint(users)
    # print([p for p in users['Users']])

    try:
        user = [
            p for p in users['Users'] 
            if p['Attributes'][0]['Value'] == user_email
        ]

        return user[0]
    except Exception as e:
        print("Failed to find user", repr(e))


def delete_user(pool_id, username):
    cognito = boto3.client('cognito-idp')

    response = cognito.admin_delete_user(
        UserPoolId=pool_id,
        Username=username
    )

    return response
