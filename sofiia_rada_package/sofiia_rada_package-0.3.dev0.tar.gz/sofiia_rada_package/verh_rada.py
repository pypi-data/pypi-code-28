from sofiia_rada_package.rada_factories import UkraineRadaFactory, PolandRadaFactory

simulation_config_file = {'rada': 'Poland'}


def main():
    if simulation_config_file['rada'] == 'Ukraine':
        UkraineRadaFactory()().run()
    else:
        PolandRadaFactory()().run()
