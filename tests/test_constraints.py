import argval.constraints as ac


def test_base_constraint():

    c = ac.Constraint()
    assert str(c) == "Constraint"


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


if __name__ == "__main__":
    print(ac.Constraint())
    print(ac.reals.IsFloat())
    ac.reals.IsFloat()(1.0)
