import os

from pandamonium import pandamon


def test_get_args():
    os.environ["USER"] = "pytest"
    args = pandamon.get_args()
    assert args.user == "pytest"
    assert args.taskname == "user.pytest"
    assert args.username == ""
