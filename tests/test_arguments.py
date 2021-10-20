import argval.arguments as aa
import argval.constraints as ac


def test_argument():

    a = aa.Argument("path", [ac.IsString(), ac.ValidPath()])
    assert a("text.txt")
    assert not a("\0_a*b:c<d>e%f/(g)h+i_0.txt")


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

    assert out0.keys() == out1.keys()
    assert out0["epoch"] == out1["epoch"]


if __name__ == "__main__":
    arg_d = {
        "path": ["IsString()", "ValidPath()"],
        "epoch": ["IsInteger()", "Positive()", ac.NonNegative()],
    }

    out = aa.get_arguments_from_dict(arg_d)
    print(out)
