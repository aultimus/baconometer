# Noddy example to demonstrate unit testing in Python
def foo():
    return 0


def test_foo():
    result = foo()
    assert result == 0
