import argval.arguments as aa
import argval.constraints as ac


def test_argument():

    a = aa.Argument("path", [ac.Required(), ac.IsString(), ac.ValidPath()])
    assert a("text.txt")
    assert not a("\0_a*b:c<d>e%f/(g)h+i_0.txt")
    assert not a(None)
    assert a.default is None

    a = aa.Argument("path", [ac.IsString(), ac.ValidPath(), ac.Default("/home/")])
    assert a("text.txt")
    assert not a("\0_a*b:c<d>e%f/(g)h+i_0.txt")
    assert a.default == "/home/"


def test_load_from_dict():

    arg_d = {
        "path": ["IsString()", "ValidPath()"],
        "epoch": ["IsInteger()", "Positive()"],
    }

    out0 = aa.get_arguments_from_dict(arg_d)

    arg_d = {
        "path": [ac.IsString(), ac.ValidPath()],
        "epoch": [ac.IsInteger(), ac.Positive()],
    }

    out1 = aa.get_arguments_from_dict(arg_d)

    assert out0 == out1


def test_validator():

    arg_d = {
        "path": ["IsString()", "ValidPath()", "Required()"],
        "epoch": ["IsInteger()", "Positive()"],
    }

    v = aa.Validator.from_dict(arg_d)

    u = aa.Validator.from_yaml(
        """---
    path:
      - IsString()
      - ValidPath()
      - Required()
    epoch:
      - IsInteger()
      - Positive()
    """
    )

    assert v == u

    for x in [v, u]:
        out = x(path="abc", epoch=1)
        assert out["path"] == "abc" and out["epoch"] == 1

        try:
            _ = x(path="abc", epoch=0)
            error = False
        except AssertionError:
            error = True
        assert error

        try:
            _ = x(epoch=10)
            error = False
        except AssertionError:
            error = True
        assert error


if __name__ == "__main__":
    arg_d = {
        "path": ["IsString()", "ValidPath()"],
        "epoch": ["IsInteger()", "Positive()", ac.NonNegative()],
    }

    out = aa.get_arguments_from_dict(arg_d)
    print(out)
