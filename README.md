# AutoArg

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
validation_manifest = """---
path:
  - IsString()
  - ValidPath()
config:
  - IsString()
  - ValidJson()
epoch:
  - Default(1)
  - IsInteger()
  - Positive()
learning_rate:
  - Default(1e-6)
  - IsFloat()
  - InRange('[ 0 , 0.1 ]', '[ 1 , oo )')
do_train:
  - IsBool()
  - Default(True)
"""

v = autoarg.Validator.from_yaml(validation_manifest)

try:
    d = v(path="/home/clarifai")
    print(d)
except Exception as e:
    print(e)

if v.args['config']('abc'):
    print("valid json")
else:
    print("invalid json")

try:
    d = v(path="/home/clarifai", config='{"model": "bert-base-cased"}')
    print(d)
except Exception as e:
    print(e)
```

## Argument Conversion

```python
conversion_manifest = """---
path: ${path}
config: ${config}
epoch: max(${epoch}, 2)
lr: max(1e-3, ${learning_rate}) if ${do_train} else 0.0
lr2: 2.5 * ${learning_rate}
"""

converter = autoarg.Converter.from_yaml(conversion_manifest)

new_values = converter(**d)
```

## Argument Filtering

```python
filtering_manifest = """---
specs:
  config: true
  epoch: true
  lr2: false
mode: normal_white
"""

filtering = autoarg.Filter.from_yaml(filtering_manifest)

filtered_values = filtering(**new_values)

blacklist = autoarg.BlackList('config', 'path')

whitelist = autoarg.WhiteList('config', 'epoch')

opposite_whitelist = ~whitelist

intersection = whitelist & blacklist

union = whitelist | blacklist
```



