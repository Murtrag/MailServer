import pytest
import users
import message
from database import domain_name

user_1 = ["test1_1234", "pass12345"]
user_2 = ["test2_1234", "pass12345"]


def setup_module(module):
    users.create_user(*user_1)
    users.create_user(*user_2)


def teardown_module(module):
    users.remove_user(*user_1)
    users.remove_user(*user_2)


@pytest.mark.messages
def test_messages():
    test_message = "test::test"
    receiver_email = f"{user_2[0]}@{domain_name}"
    message.send_message(*user_1, receiver_email, test_message)
    received_messages = [[x.title, x.message] for x in message.get_messages(*user_2)]
    assert test_message.split("::") in received_messages
