# Deploying SpotBot

These instructions are for https://www.pythonanywhere.com which is a simple Python web hosting service.
You should be able to adapt this to deploy on your host of choice.




```python
import sys
import os
from dotenv import load_dotenv
# add your project directory to the sys.path
project_home = '/home/<YOUR USERNAME>/spotbot'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path
load_dotenv(os.path.join(project_home, '.env'))
# import flask app but need to call it "application" for WSGI to work
from app import app as application  # noqa
```