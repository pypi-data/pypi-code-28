import configparser

from autolens import exc
import os
import requests
import zipfile
import shutil

directory = os.path.dirname(os.path.realpath(__file__))

CONFIG_DIR = '{}/..'.format(directory)
CONFIG_PATH = '{}/config'.format(CONFIG_DIR)

CONFIG_URL = 'https://drive.google.com/uc?authuser=0&id=1IZE4biWzuxyudDtNr4skyM0PiBHiJhBN&export=download'


class NamedConfig(object):
    """Parses generic config"""

    def __init__(self, config_path):
        """
        Parameters
        ----------
        config_path: String
            The path to the config file
        """
        self.path = config_path
        self.parser = configparser.ConfigParser()
        self.parser.read(self.path)

    def get(self, section_name, attribute_name, attribute_type=str):
        """

        Parameters
        ----------
        section_name
        attribute_type: type
            The type to which the value should be cast
        attribute_name: String
            The name of the attribute

        Returns
        -------
        prior_array: []
            An array describing a prior
        """
        string_value = self.parser.get(section_name, attribute_name)
        if string_value == "None":
            return None
        if attribute_type is bool:
            return string_value == "True"
        return attribute_type(string_value)

    def has(self, section_name, attribute_name):
        """
        Parameters
        ----------
        section_name
        attribute_name: String
            The name of the attribute

        Returns
        -------
        has_prior: bool
            True iff a prior exists for the module, class and attribute
        """
        return self.parser.has_option(section_name, attribute_name)


class AncestorConfig(object):
    """Parses prior config"""

    def __init__(self, config_folder_path):
        """
        Parameters
        ----------
        config_folder_path: String
            The path to the prior config folder
        """
        self.path = config_folder_path
        self.parser = configparser.ConfigParser()

    def read(self, module_name):
        """
        Read a particular config file

        Parameters
        ----------
        module_name: String
            The name of the module for which a config is to be read (priors relate one to one with configs).
        """
        self.parser.read("{}/{}.ini".format(self.path, module_name.split(".")[-1]))

    def get_for_nearest_ancestor(self, cls, attribute_name):
        """
        Find a prior with the attribute name from the config for this class or one of its ancestors

        Parameters
        ----------
        cls: class
            The class of interest
        attribute_name: String
            The name of the attribute
        Returns
        -------
        prior_array: []
            An array describing this prior
        """

        def family(current_class):
            yield current_class
            for next_class in current_class.__bases__:
                for val in family(next_class):
                    yield val

        for family_cls in family(cls):
            if self.has(family_cls.__module__, family_cls.__name__, attribute_name):
                return self.get(family_cls.__module__, family_cls.__name__, attribute_name)

        ini_filename = cls.__module__.split(".")[-1]
        raise exc.PriorException(
            "The prior config at {}/{} does not contain {} in {} or any of its parents".format(self.path,
                                                                                               ini_filename,
                                                                                               attribute_name,
                                                                                               cls.__name__
                                                                                               ))

    def get(self, module_name, class_name, attribute_name):
        """

        Parameters
        ----------
        module_name: String
            The name of the module
        class_name: String
            The name of the class
        attribute_name: String
            The name of the attribute

        Returns
        -------
        prior_array: []
            An array describing a prior
        """
        self.read(module_name)
        return self.parser.get(class_name, attribute_name)

    def has(self, module_name, class_name, attribute_name):
        """
        Parameters
        ----------
        module_name: String
            The name of the module
        class_name: String
            The name of the class
        attribute_name: String
            The name of the attribute

        Returns
        -------
        has_prior: bool
            True iff a prior exists for the module, class and attribute
        """
        self.read(module_name)
        return self.parser.has_option(class_name, attribute_name)


class DefaultPriorConfig(AncestorConfig):
    """Parses prior config"""

    def get(self, module_name, class_name, attribute_name):
        """

        Parameters
        ----------
        module_name: String
            The name of the module
        class_name: String
            The name of the class
        attribute_name: String
            The name of the attribute

        Returns
        -------
        prior_array: []
            An array describing a prior
        """
        arr = super(DefaultPriorConfig, self).get(module_name, class_name, attribute_name).replace(" ", "").split(",")
        return [arr[0]] + list(map(float, arr[1:]))


class WidthConfig(AncestorConfig):
    def get(self, module_name, class_name, attribute_name):
        """

        Parameters
        ----------
        module_name: String
            The name of the module
        class_name: String
            The name of the class
        attribute_name: String
            The name of the attribute

        Returns
        -------
        width: float
            The default width of a gaussian prior for this attribute
        """
        return float(super(WidthConfig, self).get(module_name, class_name, attribute_name))


def is_config(config_path=CONFIG_PATH):
    return os.path.isdir(config_path)


def download_config(config_dir=CONFIG_DIR):
    print("Downloading config...")
    config_path = '{}/config'.format(config_dir)
    zip_path = "{}.zip".format(config_path)
    with requests.get(CONFIG_URL) as response:
        with open(zip_path, 'wb') as f:
            f.write(response.content)

    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(config_dir)

    os.remove(zip_path)


def remove_config(config_path=CONFIG_PATH):
    print("Removing config...")
    try:
        shutil.rmtree(CONFIG_PATH)
    except FileNotFoundError:
        pass


class Config(object):
    def __init__(self, config_path):
        self.config_path = config_path
        self.prior_default = DefaultPriorConfig("{}/priors/default".format(config_path))
        self.prior_width = WidthConfig("{}/priors/width".format(config_path))
        self.non_linear = NamedConfig("{}/non_linear.ini".format(config_path))


instance = Config("{}/config".format(CONFIG_DIR))
