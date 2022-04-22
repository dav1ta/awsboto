
# Automatic lambda creation

create simple lambda configuration with s3 event actions with simple configurations

add configuration in config.json file

it can be multiple configuration at once

```json

[
  {
    "bucket_name": "imageprocessorbucket21",
    "event_name": "UploadEvent",
    "function_name": "imageprocessor",
    "role": "LabRole",
    "handler": "lambda_handler",
    "function_file": "lambda_func.py"
  }
]
```

save and just launch main.py

`python main.py`

there are functions maybe you can see usable

```python
from create_lambda import get_role_arn, create_lambda
from trigger import get_lambda_arn, add_trigger_s3
from bucket_create import check_or_create_bucket

# the main creation function
def create_and_assign_lambda_to_s3(
    bucket_name, event_name, function_name, role, handler, function_file
):
...

```
