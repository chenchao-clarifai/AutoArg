import argval.constraints as ac

if __name__ == "__main__":
    print(ac.Constraint())
    print(ac.reals.IsFloat())
    ac.reals.IsFloat()(1.0)
