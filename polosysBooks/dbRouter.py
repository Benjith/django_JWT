#  DB router for app1

class PolosysBooks(object):
    
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to book_db.
        """
        if model._meta.app_label == 'polosysBooks':
            return 'polosysBooksDB'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to polosysMain.
        """
        if model._meta.app_label == 'polosysBooks':
            return 'polosysBooksDB'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'polosysBooks' or \
           obj2._meta.app_label == 'polosysBooks':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'polosysMain'
        database.
        """
        if app_label == 'polosysBooks':
            return db == 'polosysBooksDB'
        return None