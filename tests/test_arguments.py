import argval.arguments as aa
import argval.constraints as ac


def test_argument():

    a = aa.Argument("path", str, [ac.ValidPath()])
    assert a("text.txt")
    assert not a("\0_a*b:c<d>e%f/(g)h+i_0.txt")


if __name__ == "__main__":
    arg_d = {
        "path": {"type": "str", "constraints": ["ValidPath()"]},
        "epoch": {"type": "int", "constraints": ["IsInteger()", "Positive()"]},
    }

    out = aa.get_arguments_from_dict(arg_d)
    print(out)
