# Import Django standard MySQL backend base
from django.db.backends.mysql import base

# Import error classes
import django.db
import MySQLdb

# Django settings to read DATABASES setting
from django.conf import settings

import logging

# Handles connecting to another available read replica or the primary database if the requested read replica fails
def get_new_connection(self, conn_params, **kwargs):
    try:
        # Get connection (call original get_new_connection method)
        conn = base.DatabaseWrapper._orig_get_new_conn(self, conn_params)
    except (django.db.OperationalError, MySQLdb.OperationalError):
        # Get read replica master DB alias (raise error if not a read replica)
        master_db = self.settings_dict.get('FAILOVER_MASTER', None)
        if not master_db:
            raise

        # DB alias from connection failure (default to current alias)
        alias = kwargs.get('failover', self.alias)

        logging.error(u'Connection error for {} ({})'.format(alias, master_db))

        # List of previously failed DBs + current failure
        failed_dbs = kwargs.get('failed_dbs', []) + [alias]

        # Get current failure retries (only increments for master)
        retries = kwargs.get('retries', 0)

        # Find a new read replica option, or default to master
        for db_alias in settings.DATABASES.keys():
            if db_alias not in failed_dbs and \
              settings.DATABASES[db_alias].get('FAILOVER_MASTER', None) == master_db:
                new_database = db_alias
                break
        else:
            # No other read replicas available - use master
            new_database = master_db

            # Master max retries on failure? Without this, we will keep retrying master until request is killed
            max_retries = settings.DATABASES[new_database].get('FAILOVER_RETRIES', None)
            if max_retries:
                # Too many failover retries? Raise error
                if retries >= max_retries:
                    raise

                retries += 1

        logging.debug(u'Custom backend chose new db: {}'.format(new_database))

        # Replace host in connection params to connect to alternate database
        conn_params['host'] = settings.DATABASES[new_database]['HOST']

        # Try new database connection
        conn = get_new_connection(self, conn_params, failover=new_database, failed_dbs=failed_dbs, retries=retries)

    return conn

# DatabaseWrapper needs to be defined so Django can import it
DatabaseWrapper = base.DatabaseWrapper

# Store a reference to get_new_connection so we can call it
base.DatabaseWrapper._orig_get_new_conn = base.DatabaseWrapper.get_new_connection

# Monkey patch get_new_connection to our function
base.DatabaseWrapper.get_new_connection = get_new_connection
