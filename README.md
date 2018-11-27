tweeter
=======

Tweeter is a basic example Django application that uses [Django Rest Framework](https://github.com/encode/django-rest-framework)

**Installation Instructions**

1. Clone the project. `git clone https://github.com/nnja/connect_python_azure`
1. `cd` intro the project directory `cd connect_python_azure`.
1. Create a new virtual environment using Python 3.7. `python3 -m venv env` and activate it with `source env/bin/activate`
1. Install dependencies from requirements.txt with `pip install -r requirements.txt`
1. Create migrations, and migrate the database. `python manage.py makemigrations` and `python manage.py migrate`
1. Run the local server via: `python manage.py runserver`
1. The local application will be available at <a href="http://localhost:8000" target="_blank">http://localhost:8000</a>

**Set up your environment variables**

See `.env-sample` for more details.

The following environment variables must be present in production:

```
# Configure the PostgreSQL Database
DB_USER="db_user"
DB_PASSWORD="db_password"
DB_NAME="db_name"
DB_HOST="db_host"

DJANGO_SETTINGS_MODULE="connect_python_azure.settings.production"
SECRET_KEY="my-secret-key"
```

Configure them in a `.secrets` file, and then `source .secrets`

**Create a production Azure PostgreSQL Server**

```
# Make sure to configure a secure admin password
POSTGRES_ADMIN_PASSWORD="secret-admin-password"

az postgres server create -u tweeteruser -n $DB_HOST --sku-name B_Gen5_1 --admin-password $POSTGRES_ADMIN_PASSWORD --resource-group appsvc_rg_linux_centralus --location "Central US"

# Create a firewall rule for your local IP
MY_IP=$(curl -s ipecho.net/plain)
# Make sure you double check the value of $MY_IP
# If you get an error saying "sql: FATAL:  no pg_hba.conf entry for host", that means the firewall entry was not correct.
az postgres server firewall-rule create --resource-group appsvc_rg_linux_centralus --server-name $DB_HOST --start-ip-address=$MY_IP --end-ip-address=$MY_IP --name AllowLocalClient

# Create a firewall rule for other azure resources
az postgres server firewall-rule create --resource-group appsvc_rg_linux_centralus --server-name $DB_HOST --start-ip-address=0.0.0.0 --end-ip-address=0.0.0.0 --name AllowAllAzureIPs

```

Next, connect to the production postgres server, create the database and configure it for Django.

```
psql -v db_password="'$DB_PASSWORD'" -h $DB_HOST.postgres.database.azure.com -U tweeteruser@$DB_HOST postgres
# Enter your PostgreSQL admin password.

Next run:
CREATE DATABASE tweeter;
CREATE USER tweeterapp WITH PASSWORD :db_password;
GRANT ALL PRIVILEGES ON DATABASE tweeter TO tweeterapp;
ALTER ROLE tweeterapp SET client_encoding TO 'utf8';
ALTER ROLE tweeterapp SET default_transaction_isolation TO 'read committed';
ALTER ROLE tweeterapp SET timezone TO 'UTC';
\q
```

Lastly,
```
# export all the environment variables in .secrets
set -a; source .secrets; set +a
python manage.py migrate
```

**Configure Production app settings from file**
```
# Edit APP_SERVICE_NAME to the name of your deployment.
# Optionally pipe to /dev/null to avoid printing the secret values in your terminal.

APP_SERVICE_NAME="connect-python-azure-test"
az webapp config appsettings set --resource-group appsvc_rg_linux_centralus --name $APP_SERVICE_NAME --settings $(grep -v '^#' .secrets | xargs)  > /dev/null
# To confirm the secrets were set successfully, run:
echo $?
# The value should be 0.
```