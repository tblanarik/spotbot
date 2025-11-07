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


## DB

may need to step a MySQL password?

Create DB then create table:

```sql
CREATE TABLE spots(
    callsign VARCHAR(255),
    message_id text,
    utctimestamp timestamp
);
```


## .env file

Create a .env file at `/home/<YOU>/<repo>/.env`

Fill it out:

```bash
export TARGET_URL=https://discord.com/api/webhooks/...
export LOOKBACK_SECONDS=7200
export SECRET_ENDPOINT=abcdefg12345
export MYSQL_HOST=<YOU>.mysql.pythonanywhere-services.com
export MYSQL_USER=<YOU>
export MYSQL_PASSWORD=<PASSWORD>
export MYSQL_DATABASE=<YOU>$<DB NAME>
```