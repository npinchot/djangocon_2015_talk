import random
from django.conf import settings

class ReadReplicaRouter(object):
    def db_for_read(self, model, **hints):
        # Reads go to a randomly-chosen replica.
        return random.choice(settings.READ_REPLICAS)

    def db_for_write(self, model, **hints):
        # Writes always go to default.
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Relations are allowed if both objects are in default/replica pool.
        db_list = ('default', settings.READ_REPLICAS)
        return obj1._state.db in db_list and obj2._state.db in db_list

    def allow_migrate(self, db, app_label, model=None, **hints):
        return True
