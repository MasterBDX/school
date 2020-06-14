from django.apps import AppConfig


class SchoolTabelsConfig(AppConfig):
    name = 'school_tables'

    def ready(self):
        import school_tables.signals
