import argval.constraints as ac


def test_base_constraint():

    c = ac.Constraint()
    assert str(c) == "Constraint()"


def test_isinstance():

    c = ac.IsInstance(str)
    assert c("abc")
    assert not c(1.0)
    assert str(c) == f"IsInstance({str})"

    c = ac.IsInstance(
        (
            int,
            float,
        )
    )
    assert not c("abc")
    assert c(1.0) and c(1)
    assert str(c) == f"IsInstance({(int, float,)})"


def test_reals():

    c = ac.IsFloat()
    assert c(1.0)
    assert not c(1)

    c = ac.IsInteger()
    assert c(1)
    assert not c(1.0)

    c = ac.InRange("[ 0 , 1 ]")
    assert c(0.5)
    assert c(0) and c(1)
    assert not c(-1)
    assert not c(1.1)

    c = ac.InRange("[ 0 , 1 )")
    assert c(0.5)
    assert c(0) and not c(1)
    assert not c(-1)
    assert not c(1.1)

    c = ac.InRange("[ 0 , 1 )", "[ 2 , oo ]")
    assert c(0.5)
    assert c(0) and not c(1)
    assert not c(-1)
    assert not c(1.1)
    assert c(2) and c(3.5)


def test_strings():

    c = ac.IsString()
    assert c("abc")
    assert not c(1)

    c = ac.ValidPath("linux")
    assert c("/usr/share")
    assert c("file.txt")
    assert not c("\0_a*b:c<d>e%f/(g)h+i_0.txt")


def test_logicals():

    c = ac.NOT(ac.IsFloat())
    assert c(1) and c("abc")
    assert not c(1.0)

    c = ac.ANY(ac.IsFloat(), ac.IsInteger())
    assert c(1.0) and c(1)
    assert not c("abc")

    c = ac.ALL(ac.IsFloat(), ac.IsInteger())
    assert not c(1.0)
    assert not c(1)


def test_equal():

    assert ac.IsInteger() == ac.IsInteger()
    assert ac.IsInteger() != ac.IsFloat()
    assert ac.IsFloat() == ac.IsFloat()
    assert ac.InRange("[ 0 , 1 ]") == ac.InRange("[ 0 , 1 ]")
    assert ac.InRange("[ 0 , 1 ]") != ac.InRange("[ 0 , 1 )")


if __name__ == "__main__":
    c = ac.InRange("[ 0 , 1 ]", "[ 0 , 1 ]")
    print(c(0.5))
    assert c(0.5)
    assert c(0) and c(1)
    assert not c(-1)
    assert not c(1.1)
