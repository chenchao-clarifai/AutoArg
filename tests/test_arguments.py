import autoarg.arguments as aa
import autoarg.constraints as ac


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


def test_converter():

    arg_d = {
        "path": "${a}/${b}",
        "epoch": "$c + $d",
    }

    v = aa.Converter.from_dict(arg_d)

    u = aa.Converter.from_yaml(
        """---
    path: ${a}/${b}
    epoch: $c + $d
    """
    )

    assert v == u

    for x in [u, v]:
        out = x(a="home", b="src", c=1, d=2)
        assert out["path"] == "home/src" and out["epoch"] == 3


def test_filters():
    f = aa.Filter.from_yaml(
        """---
    specs:
      var1: True
      var2: True
      var3: False
    mode: normal_black
    """
    )

    d = f(var1=1, var2=2, var3=3, var4=4, var5=5)
    assert "var1" in d and d["var1"] == 1
    assert "var2" in d and d["var2"] == 2
    assert "var3" not in d
    assert "var4" not in d
    assert "var5" not in d

    f = aa.Filter.from_yaml(
        """---
    specs:
      var1: True
      var2: True
      var3: False
    mode: normal_white
    """
    )

    d = f(var1=1, var2=2, var3=3, var4=4, var5=5)
    assert "var1" in d and d["var1"] == 1
    assert "var2" in d and d["var2"] == 2
    assert "var3" not in d
    assert "var4" in d and d["var4"] == 4
    assert "var5" in d and d["var5"] == 5

    f1 = aa.Filter.from_yaml(
        """
    specs:
      var1: True
      var2: True
    mode: normal_black
    """
    )

    assert f1 == aa.WhiteList(["var1", "var2"])


if __name__ == "__main__":
    arg_d = {
        "path": ["IsString()", "ValidPath()"],
        "epoch": ["IsInteger()", "Positive()", ac.NonNegative()],
    }

    out = aa.get_arguments_from_dict(arg_d)
    print(out)
