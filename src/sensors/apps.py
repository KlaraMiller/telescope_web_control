from django.apps import AppConfig

def startup():
    print('STARTUP SensorsApp')

class SensorsConfig(AppConfig):
    name = 'sensors'