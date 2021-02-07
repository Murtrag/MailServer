import pytest
import clcrypto


@pytest.mark.clcrypto
def test_generate_salt():
    salt = clcrypto.generate_salt()
    assert type(salt) == str
    assert len(salt) == 16


@pytest.mark.clcrypto
def test_password_hash():
    hash = clcrypto.password_hash("test1234", clcrypto.generate_salt())
    assert type(hash) == str
    assert len(hash) == 80

    hash = clcrypto.password_hash(
        "test1234",
    )
    assert type(hash) == str
    assert len(hash) == 80


@pytest.mark.clcrypto
def test_check_password():
    password = "test1234"
    hash = clcrypto.password_hash(password)
    assert True is clcrypto.check_password(password, hash)
    assert False is clcrypto.check_password(password + "incorrect string", hash)


@pytest.mark.clcrypto
def test_check_pass_len():
    assert True is clcrypto.check_pass_len("asdfghjk")
    assert False is clcrypto.check_pass_len("as12")


@pytest.mark.clcrypto
def test_slice_args():
    test_args = ["main.py", "-u", "test1", "-d", "-p", "pass12"]
    sliced_args = clcrypto.slice_args(test_args)
    assert sliced_args["-u"] == "test1"
    assert sliced_args["-p"] == "pass12"
    assert sliced_args["-d"] is None
