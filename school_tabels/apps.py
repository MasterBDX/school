from django.apps import AppConfig


class SchoolTabelsConfig(AppConfig):
    name = 'school_tabels'

    def ready(self):
        import school_tabels.signals
