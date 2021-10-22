# AutoArgs

```shell
├── README.md
├── argval
│   ├── __init__.py
│   ├── arguments.py
│   └── constraints
│       ├── __init__.py
│       ├── base.py
│       ├── inputs.py
│       ├── logicals.py
│       ├── reals.py
│       └── strings.py
├── requirements.txt
├── setup.py
└── tests
    ├── test_arguments.py
    └── test_constraints.py
```

## Argument Validation

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

validation_yaml = """---
    path:
      - IsString()
      - ValidPath()
    epoch:
      - IsInteger()
      - Positive()
      - Default(1)
    lr:
      - IsFloat()
      - InRange('[ 0 , 1 ]')
      - Default(1e-6)
    size:
      - IsInteger()
      - Positive()
    """
ex = yaml.safe_load(validation_yaml)
args = aa.get_arguments_from_dict(ex)

"""
=================
args['epoch'](0)
>> False
args['epoch'](1.0)
>> False
args['epoch'](1)
>> True
"""

validator = aa.Validator.from_yaml(validation_yaml)
valid_value_dict = validator(path='/root/', size=128)
```

## Argument Conversion

```python
conversion_yaml = """---
		checkpoint_path: ${path}
		epoch: ${epoch}
		lr: min(${lr}, 1e-5)
		size: (${size}, ${size})
		"""

converter = aa.Converter.from_yaml(conversion_yaml)
converted_value_dict = converter(valid_value_dict)
```

