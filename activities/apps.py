from django.apps import AppConfig


class ActivitiesConfig(AppConfig):
    name = 'activities'

    def ready(self) -> None:
        import activities.signals
