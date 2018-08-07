# -*- coding: utf-8 -*-


# Copyright (c) 2016  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Written by Petr Šabata <contyk@redhat.com>
#            Filip Valder <fvalder@redhat.com>

import imp
import os
import pkg_resources
import re
import sys

from module_build_service import logger


# TODO: It'd be nice to reuse this from models.ModuleBuild.rebuild_strategies but models.py
# currently relies on this file, so we can't import it
SUPPORTED_STRATEGIES = ['changed-and-after', 'only-changed', 'all']

SUPPORTED_RESOLVERS = {
    'mbs': {'builders': ['mock']},
    'db': {'builders': ['koji', 'mock', 'copr']}
}


def init_config(app):
    """ Configure MBS and the Flask app
    """
    config_module = None
    config_file = '/etc/module-build-service/config.py'
    config_section = 'DevConfiguration'

    # automagically detect production environment:
    #   - existing and readable config_file presets ProdConfiguration
    try:
        with open(config_file):
            config_section = 'ProdConfiguration'
    except Exception:
        pass
    #   - Flask app within mod_wsgi presets ProdConfiguration
    flask_app_env = hasattr(app, 'request') and hasattr(app.request, 'environ')
    if flask_app_env and any([var.startswith('mod_wsgi.')
                              for var in app.request.environ]):
        config_section = 'ProdConfiguration'

    # Load LocalBuildConfiguration section in case we are building modules
    # locally.
    if "build_module_locally" in sys.argv:
        config_section = "LocalBuildConfiguration"

    # try getting config_file from os.environ
    if 'MBS_CONFIG_FILE' in os.environ:
        config_file = os.environ['MBS_CONFIG_FILE']
    # try getting config_section from os.environ
    if 'MBS_CONFIG_SECTION' in os.environ:
        config_section = os.environ['MBS_CONFIG_SECTION']
    # preferably get these values from Flask app
    if flask_app_env:
        # try getting config_file from Flask app
        if 'MBS_CONFIG_FILE' in app.request.environ:
            config_file = app.request.environ['MBS_CONFIG_FILE']
        # try getting config_section from Flask app
        if 'MBS_CONFIG_SECTION' in app.request.environ:
            config_section = app.request.environ['MBS_CONFIG_SECTION']
    # TestConfiguration shall only be used for running tests, otherwise...
    if any(['py.test' in arg or 'pytest' in arg for arg in sys.argv]):
        config_section = 'TestConfiguration'
        from conf import config
        config_module = config
    # ...MODULE_BUILD_SERVICE_DEVELOPER_ENV has always the last word
    # and overrides anything previously set before!
    # Again, check Flask app (preferably) or fallback to os.environ.
    # In any of the following cases, use configuration directly from MBS package
    # -> /conf/config.py.
    elif (flask_app_env and
          'MODULE_BUILD_SERVICE_DEVELOPER_ENV' in app.request.environ):
        if app.request.environ['MODULE_BUILD_SERVICE_DEVELOPER_ENV'].lower() in (
                '1', 'on', 'true', 'y', 'yes'):
            config_section = 'DevConfiguration'
            from conf import config
            config_module = config
    elif ('MODULE_BUILD_SERVICE_DEVELOPER_ENV' in os.environ and
          os.environ['MODULE_BUILD_SERVICE_DEVELOPER_ENV'].lower() in (
            '1', 'on', 'true', 'y', 'yes')):
        config_section = 'DevConfiguration'
        from conf import config
        config_module = config
    # try loading configuration from file
    if not config_module:
        try:
            config_module = imp.load_source('mbs_runtime_config',
                                            config_file)
        except Exception:
            raise SystemError("Configuration file {} was not found."
                              .format(config_file))

    # finally configure MBS and the Flask app
    config_section_obj = getattr(config_module, config_section)
    conf = Config(config_section_obj)
    app.config.from_object(config_section_obj)
    return conf


class Path:
    """
    Config type for paths. Expands the users home directory.
    """
    pass


class Config(object):
    """Class representing the orchestrator configuration."""
    _defaults = {
        'debug': {
            'type': bool,
            'default': False,
            'desc': 'Debug mode'},
        'system': {
            'type': str,
            'default': 'koji',
            'desc': 'The buildsystem to use.'},
        'db': {
            'type': str,
            'default': '',
            'desc': 'RDB URL.'},
        'default_dist_tag_prefix': {
            'type': str,
            'default': 'module+',
            'desc': 'Default dist-tag prefix for built modules.'},
        'polling_interval': {
            'type': int,
            'default': 0,
            'desc': 'Polling interval, in seconds.'},
        'cache_dir': {
            'type': Path,
            'default': '~/modulebuild/cache',
            'desc': 'Cache directory'},
        'mbs_url': {
            'type': str,
            'default': 'https://mbs.fedoraproject.org/module-build-service/1/module-builds/',
            'desc': 'MBS instance url for MBSResolver'},
        'koji_config': {
            'type': str,
            'default': None,
            'desc': 'Koji config file.'},
        'koji_profile': {
            'type': str,
            'default': None,
            'desc': 'Koji config profile.'},
        'koji_arches': {
            'type': list,
            'default': [],
            'desc': 'Koji architectures.'},
        'koji_build_priority': {
            'type': int,
            'default': 10,
            'desc': ''},
        'koji_repository_url': {
            'type': str,
            'default': None,
            'desc': 'Koji repository URL.'},
        'koji_build_macros_target': {
            'type': str,
            'default': '',
            'desc': 'Target to build "module-build-macros" RPM in.'},
        'koji_tag_prefixes': {
            'type': list,
            'default': ['module'],
            'desc': 'List of allowed koji tag prefixes.'},
        'koji_target_delete_time': {
            'type': int,
            'default': 24 * 3600,
            'desc': 'Time in seconds after which the Koji target of '
                    'built module is deleted'},
        'koji_enable_content_generator': {
            'type': bool,
            'default': True,
            'desc': 'Enable or disable imports to koji using content '
                    'generator api'},
        'allow_custom_scmurls': {
            'type': bool,
            'default': False,
            'desc': 'Allow custom scmurls.'},
        'rpms_default_repository': {
            'type': str,
            'default': 'git://pkgs.fedoraproject.org/rpms/',
            'desc': 'RPMs default repository URL.'},
        'rpms_allow_repository': {
            'type': bool,
            'default': False,
            'desc': 'Allow custom RPMs repositories.'},
        'rpms_default_cache': {
            'type': str,
            'default': 'http://pkgs.fedoraproject.org/repo/pkgs/',
            'desc': 'RPMs default cache URL.'},
        'rpms_allow_cache': {
            'type': bool,
            'default': False,
            'desc': 'Allow custom RPMs cache.'},
        'modules_default_repository': {
            'type': str,
            'default': 'git://pkgs.fedoraproject.org/modules/',
            'desc': 'Included modules default repository URL.'},
        'modules_allow_repository': {
            'type': bool,
            'default': False,
            'desc': 'Allow custom included modules repositories.'},
        'allowed_groups': {
            'type': set,
            'default': set(['packager']),
            'desc': 'The set of groups allowed to submit builds.'},
        'log_backend': {
            'type': str,
            'default': None,
            'desc': 'Log backend'},
        'log_file': {
            'type': str,
            'default': '',
            'desc': 'Path to log file'},
        'log_level': {
            'type': str,
            'default': 0,
            'desc': 'Log level'},
        'build_logs_dir': {
            'type': Path,
            'default': "",
            'desc': 'Directory to store module build logs to.'},
        'build_logs_name_format': {
            'type': str,
            'default': "build-{id}.log",
            'desc': ('Format of a module build log\'s name. Use `Build` attributes as formatting '
                     'kwargs')},
        'krb_keytab': {
            'type': None,
            'default': None,
            'desc': ''},
        'krb_principal': {
            'type': None,
            'default': None,
            'desc': ''},
        'krb_ccache': {
            'type': None,
            'default': '/tmp/krb5cc_module_build_service',
            'desc': ''},
        'messaging': {
            'type': str,
            'default': 'fedmsg',
            'desc': 'The messaging system to use.'},
        'messaging_topic_prefix': {
            'type': list,
            'default': ['org.fedoraproject.prod'],
            'desc': 'The messaging system topic prefixes which we are interested in.'},
        'amq_recv_addresses': {
            'type': list,
            'default': [],
            'desc': 'Apache MQ broker url to receive messages.'},
        'amq_dest_address': {
            'type': str,
            'default': '',
            'desc': 'Apache MQ broker address to send messages'},
        'amq_cert_file': {
            'type': str,
            'default': '',
            'desc': 'Certificate for Apache MQ broker auth.'},
        'amq_private_key_file': {
            'type': str,
            'default': '',
            'desc': 'Private key for Apache MQ broker auth.'},
        'amq_trusted_cert_file': {
            'type': str,
            'default': '',
            'desc': 'Trusted certificate for ssl connection.'},
        'distgits': {
            'type': dict,
            'default': {
                'git://pkgs.fedoraproject.org': ('fedpkg clone --anonymous {}',
                                                 'fedpkg --release module sources'),
            },
            'desc': 'Mapping between dist-git and command to '},
        'mock_config': {
            'type': str,
            'default': 'fedora-25-x86_64',
            'desc': ''},
        'mock_config_file': {
            'type': list,
            'default': ['/etc/module-build-service/mock.cfg', 'conf/mock.cfg'],
            'desc': 'List of mock config file paths in order of preference.'},
        'mock_build_srpm_cmd': {
            'type': str,
            'default': 'fedpkg --release f26 srpm',
            'desc': ''},
        'mock_resultsdir': {
            'type': Path,
            'default': '~/modulebuild/builds',
            'desc': 'Directory for Mock build results.'},
        'mock_purge_useless_logs': {
            'type': bool,
            'default': True,
            'desc': 'Remove empty or otherwise useless log files.'},
        'arch_autodetect': {
            'type': bool,
            'default': True,
            'desc': 'Auto-detect machine arch when configuring builder.'},
        'arch_fallback': {
            'type': str,
            'default': 'x86_64',
            'desc': 'Fallback arch if auto-detection is off or unable to determine it.'},
        'scmurls': {
            'type': list,
            'default': [],
            'desc': 'Allowed SCM URLs for submitted module.'},
        'yaml_submit_allowed': {
            'type': bool,
            'default': False,
            'desc': 'Is it allowed to directly submit modulemd yaml file?'},
        'num_concurrent_builds': {
            'type': int,
            'default': 0,
            'desc': 'Number of concurrent component builds.'},
        'net_timeout': {
            'type': int,
            'default': 120,
            'desc': 'Global network timeout for read/write operations, in seconds.'},
        'net_retry_interval': {
            'type': int,
            'default': 30,
            'desc': 'Global network retry interval for read/write operations, in seconds.'},
        'scm_net_timeout': {
            'type': int,
            'default': 60,
            'desc': 'Network timeout for SCM operations, in seconds.'},
        'scm_net_retry_interval': {
            'type': int,
            'default': 15,
            'desc': 'Network retry interval for SCM operations, in seconds.'},
        'no_auth': {
            'type': bool,
            'default': False,
            'desc': 'Disable client authentication.'},
        'admin_groups': {
            'type': set,
            'default': set([]),
            'desc': 'The set of groups allowed to manage MBS.'},
        'yum_config_file': {
            'type': list,
            'default': ['/etc/module-build-service/yum.conf', 'conf/yum.conf'],
            'desc': 'List of yum config file paths in order of preference.'},
        'auth_method': {
            'type': str,
            'default': 'oidc',
            'desc': 'Authentiation method to MBS. Options are oidc or kerberos'},
        'kerberos_http_host': {
            'type': str,
            'default': '',
            'desc': ('Hardcodes the HTTP host MBS identifies as in Kerberos. If this isn\'t set, '
                     'it will be derived dynamically.')},
        'kerberos_keytab': {
            'type': str,
            'default': '',
            'desc': ('Overrides the use of the environment variable KRB5_KTNAME, which specifies '
                     'the location to the Kerberos keytab for authentication.')},
        'ldap_uri': {
            'type': str,
            'default': '',
            'desc': 'LDAP URI to query for group information when using Kerberos authentication'},
        'ldap_groups_dn': {
            'type': str,
            'default': '',
            'desc': ('The distinguished name of the container or organizational unit containing '
                     'the groups in LDAP')},
        'base_module_names': {
            'type': set,
            'default': set(['platform', 'bootstrap']),
            'desc': ("Set of module names which defines the product version "
                     "(by their stream) of modules depending on them.")},
        'koji_cg_build_tag_template': {
            'type': str,
            'default': "{}-modular-updates-candidate",
            'desc': "Name of a Koji tag where the top-level Content Generator "
                    "build is tagged to. The '{}' string is replaced by a "
                    "stream name of a base module on top of which the "
                    "module is built."},
        'koji_cg_default_build_tag': {
            'type': str,
            'default': "modular-updates-candidate",
            'desc': "The name of Koji tag which should be used as fallback "
                    "when koji_cg_build_tag_template tag is not found in "
                    "Koji."},
        'rebuild_strategy': {
            'type': str,
            'default': 'changed-and-after',
            'desc': 'The module rebuild strategy to use by default.'},
        'rebuild_strategy_allow_override': {
            'type': bool,
            'default': False,
            'desc': ('Allows a user to specify the rebuild strategy they want to use when '
                     'submitting a module build.')},
        'rebuild_strategies_allowed': {
            'type': list,
            'default': SUPPORTED_STRATEGIES,
            'desc': ('The allowed module rebuild strategies. This is only used when '
                     'REBUILD_STRATEGY_ALLOW_OVERRIDE is True.')},
        'cleanup_failed_builds_time': {
            'type': int,
            'default': 180,
            'desc': ('Time in days when to cleanup failed module builds and transition them to '
                     'the "garbage" state.')},
        'resolver': {
            'type': str,
            'default': 'db',
            'desc': 'Where to look up for modules. Note that this can (and '
                    'probably will) be builder-specific.'},
    }

    def __init__(self, conf_section_obj):
        """
        Initialize the Config object with defaults and then override them
        with runtime values.
        """

        # set defaults
        for name, values in self._defaults.items():
            self.set_item(name, values['default'], values['type'])

        # override defaults
        for key in dir(conf_section_obj):
            # skip keys starting with underscore
            if key.startswith('_'):
                continue
            # set item (lower key)
            self.set_item(key.lower(), getattr(conf_section_obj, key))

    def set_item(self, key, value, value_type=None):
        """
        Set value for configuration item. Creates the self._key = value
        attribute and self.key property to set/get/del the attribute.
        """
        if key == 'set_item' or key.startswith('_'):
            raise Exception("Configuration item's name is not allowed: %s" % key)

        # Create the empty self._key attribute, so we can assign to it.
        if not hasattr(self, "_" + key):
            setattr(self, "_" + key, None)

            # Create self.key property to access the self._key attribute.
            # Use the setifok_func if available for the attribute.
            setifok_func = '_setifok_{}'.format(key)
            if hasattr(self, setifok_func):
                setx = lambda self, val: getattr(self, setifok_func)(val)
            elif value_type == Path:
                # For paths, expanduser.
                setx = lambda self, val: setattr(
                    self, "_" + key, os.path.expanduser(val))
            else:
                setx = lambda self, val: setattr(self, "_" + key, val)
            getx = lambda self: getattr(self, "_" + key)
            delx = lambda self: delattr(self, "_" + key)
            setattr(Config, key, property(getx, setx, delx))

        # managed/registered configuration items
        if key in self._defaults:
            # type conversion for configuration item
            convert = self._defaults[key]['type']
            if convert in [bool, int, list, str, set, dict]:
                try:
                    # Do no try to convert None...
                    if value is not None:
                        value = convert(value)
                except Exception:
                    raise TypeError("Configuration value conversion failed for name: %s" % key)
            # unknown type/unsupported conversion, or conversion not needed
            elif convert is not None and convert not in [Path]:
                raise TypeError("Unsupported type %s for configuration item name: %s"
                                % (convert, key))

        # Set the attribute to the correct value
        setattr(self, key, value)

    #
    # Register your _setifok_* handlers here
    #

    def _setifok_system(self, s):
        s = str(s)
        if s not in ("koji", "mock"):
            raise ValueError("Unsupported buildsystem: %s." % s)
        self._system = s

    def _setifok_polling_interval(self, i):
        if not isinstance(i, int):
            raise TypeError("polling_interval needs to be an int")
        if i < 0:
            raise ValueError("polling_interval must be >= 0")
        self._polling_interval = i

    def _setifok_rpms_default_repository(self, s):
        rpm_repo = str(s)
        rpm_repo = rpm_repo.rstrip('/') + '/'
        self._rpms_default_repository = rpm_repo

    def _setifok_rpms_default_cache(self, s):
        rpm_cache = str(s)
        rpm_cache = rpm_cache.rstrip('/') + '/'
        self._rpms_default_cache = rpm_cache

    def _setifok_log_backend(self, s):
        if s is None:
            self._log_backend = "console"
        elif s not in logger.supported_log_backends():
            raise ValueError("Unsupported log backend")
        self._log_backend = str(s)

    def _setifok_log_file(self, s):
        if s is None:
            self._log_file = ""
        else:
            self._log_file = str(s)

    def _setifok_log_level(self, s):
        level = str(s).lower()
        self._log_level = logger.str_to_log_level(level)

    def _setifok_messaging(self, s):
        """ Validate that the specified messaging backend corresponds with one
        of the installed plugins.  The MBS core provides two such plugins, but
        a third-party could install another usable one.
        """
        entrypoints = pkg_resources.iter_entry_points('mbs.messaging_backends')
        installed_backends = [e.name for e in entrypoints]
        s = str(s)
        if s not in installed_backends:
            raise ValueError('The messaging plugin for "{0}" is not installed.'
                             ' The following are installed: {1}'
                             .format(s, ', '.join(installed_backends)))
        self._messaging = s

    def _setifok_amq_recv_addresses(self, l):
        assert isinstance(l, list) or isinstance(l, tuple)
        self._amq_recv_addresses = list(l)

    def _setifok_scmurls(self, l):
        if not isinstance(l, list):
            raise TypeError("scmurls needs to be a list.")
        self._scmurls = [str(x) for x in l]

    def _setifok_num_concurrent_builds(self, i):
        if not isinstance(i, int):
            raise TypeError('NUM_CONCURRENT_BUILDS needs to be an int')
        if i < 0:
            raise ValueError('NUM_CONCURRENT_BUILDS must be >= 0')
        self._num_concurrent_builds = i

    def _setifok_auth_method(self, s):
        s = str(s)
        if s.lower() not in ('oidc', 'kerberos'):
            raise ValueError('Unsupported authentication method')
        if s.lower() == 'kerberos':
            try:
                import ldap3  # noqa
            except ImportError:
                raise ValueError("ldap3 is required for kerberos authz")
        self._auth_method = s.lower()

    def _setifok_kerberos_keytab(self, s):
        keytab = str(s)
        if keytab:
            keytab = os.path.expanduser(keytab)
            if not os.path.exists(keytab):
                raise ValueError('The path set for KERBEROS_KEYTAB does not exist')

        self._kerberos_keytab = keytab

    def _setifok_ldap_uri(self, s):
        ldap_uri = str(s)

        if ldap_uri and not re.match(r'^(?:ldap(?:s)?:\/\/.+)$', ldap_uri):
            raise ValueError('LDAP_URI is invalid. It must start with "ldap://" or "ldaps://"')

        self._ldap_uri = ldap_uri

    def _setifok_rebuild_strategy(self, strategy):
        if strategy not in SUPPORTED_STRATEGIES:
            raise ValueError('The strategy "{0}" is not supported. Choose from: {1}'
                             .format(strategy, ', '.join(SUPPORTED_STRATEGIES)))
        self._rebuild_strategy = strategy

    def _setifok_rebuild_strategies_allowed(self, strategies):
        if not isinstance(strategies, list):
            raise ValueError('REBUILD_STRATEGIES_ALLOWED must be a list')
        elif not strategies:
            raise ValueError('REBUILD_STRATEGIES_ALLOWED must contain at least one rebuild '
                             'strategy')
        for strategy in strategies:
            if strategy not in SUPPORTED_STRATEGIES:
                raise ValueError('REBUILD_STRATEGIES_ALLOWED must be one of: {0}'
                                 .format(', '.join(SUPPORTED_STRATEGIES)))

        self._rebuild_strategies_allowed = strategies

    def _setifok_cleanup_failed_builds_time(self, num_days):
        if num_days < 1:
            raise ValueError('CLEANUP_FAILED_BUILDS_TIME must be set to 1 or more days')
        self._cleanup_failed_builds_time = num_days

    def _setifok_resolver(self, s):
        if s not in SUPPORTED_RESOLVERS.keys():
            raise ValueError('The resolver "{0}" is not supported. Choose from: {1}'
                             .format(s, ', '.join(SUPPORTED_RESOLVERS.keys())))
        self._resolver = s
