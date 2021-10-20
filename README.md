# Argument Validation

```
argval
├── __init__.py
├── arguments.py
└── constraints
    ├── __init__.py
    ├── base.py
    ├── logicals.py
    ├── reals.py
    └── strings.py
```

Example

```yaml
path:
  - IsString()
  - ValidPath()
epoch:
  - IsInteger()
  - Positive()
lr:
  - IsFloat()
  - InRange('[ 0 , 1 ]')
size:
  - IsInteger()
  - Positive()
```

```Python
import argval
import argval.constraints as ac
import argval.arguments as aa


ex = yaml.safe_load(
    """---
    path:
      - IsString()
      - ValidPath()
    epoch:
      - IsInteger()
      - Positive()
    lr:
      - IsFloat()
      - InRange('[ 0 , 1 ]')
    size:
      - IsInteger()
      - Positive()
    """
)


args = aa.get_arguments_from_dict(ex)


# Is valid
=================
args['epoch'](0)
>> False
args['epoch'](1.0)
>> False
args['epoch'](1)
>> True

```
