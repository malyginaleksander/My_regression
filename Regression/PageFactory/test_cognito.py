
from Regression.PageFactory.cognito_services import get_pool_id, get_user, delete_user


def test_user():
    pool = get_pool_id('ecc-qa-nrg_residential')
    user = get_user(pool, 'ksgurjeetsaini9@gmail.com')

    if user:
        assert user['Username']

        response = delete_user(pool, user['Username'])
        print(user)
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200
        print('deleted')
    #else:
       # print('I ain\'t found no user.')