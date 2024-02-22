# iot-vas

## TODO

|To Do|Doing|Done|
|-|-|-|
|Database schema                             |Make API require auth|Replace sqlite with postgresql|
|Devices page                                |                     |Replace ORM with psycopg      |
|Reports page                                |                     |                              |
|Overview page                               |                     |                              |
|Admin page for managing gvm and psql backend|                     |                              |

## Creating updated requirements.txt

If you want to update requirements.txt, make a new virtual environment and then install the required packages using pip. It may be necessary to put quotes around the psycopg[binary] package like so:

```shell
pip install 'Flask' 'Flask-Login' 'psycopg[binary]' 'python-gvm'
```

Then you can use pip freeze to update requirements.txt like so:

```shell
pip freeze > requirements.txt
```
