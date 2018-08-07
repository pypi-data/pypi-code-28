#
# Copyright (c) 2016-2017 Illumon and Patent Pending
#

import jpy
import jpyutil
import os
import os.path
from glob import glob
import re

import iris

def start_jvm(devroot=None,
              workspace=None,
              propfile=None,
              keyfile=None,
              verbose=False,
              skip_default_classpath=None,
              # The following are the jpyutil.init_jvm options which are passed through after attaching our options
              java_home=None,
              jvm_dll=None,
              jvm_maxmem=None,
              jvm_classpath=None,
              jvm_properties=None,
              jvm_options=None,
              config_file=None,
              config=None):
    """ Starts a JVM within this Python process to interface with Illumon Iris.

        This is a small convenience wrapper around jpyutil.init_jvm.
        Additionally, the Configuration is loaded and and Iris classes are brought into Python.

        :param devroot the devroot parameter for Iris; defaults to the ILLUMON_DEVROOT environment variable, or /usr/illumon/latest
        :param workspace the workspace parameter for Iris; defaults to the ILLUMON_WORKSPACE environment variable
        :param propfile the Configuration.rootFile parameter for Iris; defaults to the ILLUMON_PROPFILE environment variable
        :param keyfile your private key file for authenticating to Iris
        :param skip_default_classpath if True, do not attempt to compute default java classpath
        :param verbose if True, print out the classpath and properties we have constructed

        The rest of the parameters are passed through to jpyutil.init_jvm; the
        jvm_classpath and jvm_properties may have been modified by other
        start_jvm arguments.

        :param java_home
        :param jvm_dll
        :param jvm_maxmem
        :param jvm_classpath optional initial classpath elements; default elements will be appended unless skip_default_classpath is specified
        :param jvm_properties inserted into the dictionary generated by devroot, workspace, propfile, and keyfile.
        :param jvm_options
        :param config_file
        :param config
    """

    # setup defaults

    if devroot is None and "ILLUMON_DEVROOT" in os.environ:
        devroot = os.environ["ILLUMON_DEVROOT"]
    if devroot is None and os.path.isdir("/usr/illumon/latest"):
        devroot = "/usr/illumon/latest"

    if devroot is None:
        raise IOError("idb.init: devroot is not specified.")
    if not os.path.isdir(devroot):
        raise IOError("idb.init: devroot=%s does not exist." % devroot)

    if workspace is None and "ILLUMON_WORKSPACE" in os.environ:
        workspace = os.environ["ILLUMON_WORKSPACE"]

    if workspace is None:
        raise IOError("idb.init: workspace is not specified.")
    if not os.path.isdir(workspace):
        raise IOError("idb.init: workspace=%s does not exist." % workspace)

    if propfile is None and "ILLUMON_PROPFILE" in os.environ:
        propfile = os.environ["ILLUMON_PROPFILE"]

    # setup environment

    jProperties = {}
    jProperties['devroot'] = devroot
    jProperties['workspace'] = workspace
    if propfile is not None:
        jProperties['Configuration.rootFile'] = propfile
    if keyfile is not None:
        jProperties['WAuthenticationClientManager.defaultPrivateKeyFile'] = keyfile
    if jvm_properties is not None:
        jProperties.update(jvm_properties)

    jClassPath = []

    # allow for string or array, because users get confused
    if jvm_classpath is not None:
        if isinstance(jvm_classpath, basestring):
            jClassPath.extend(jvm_classpath.split(os.path.pathsep))
        else:
            jClassPath.extend(jvm_classpath)

    defaultClasspath = None
    if not skip_default_classpath:
        defaultClasspath = getDefaultClasspath(devroot, workspace)
        jClassPath.extend(defaultClasspath)

    jClassPath = expandWildcardsInList(jClassPath)

    if verbose:
        print("JVM default classpath...%s" % defaultClasspath)
        print("JVM classpath...%s" % jClassPath)
        print("JVM properties...%s" % jProperties)

    jpy.VerboseExceptions.enabled = True
    jpyutil.init_jvm(
        java_home=java_home,
        jvm_dll=jvm_dll,
        jvm_maxmem=jvm_maxmem,
        jvm_classpath=jClassPath,
        jvm_properties=jProperties,
        jvm_options=jvm_options,
        config_file=config_file,
        config=config)

    # Loads our configuration and initializes the class types

    iris.initialize()


def getDefaultClasspath(devroot, workspace):
    """
    Figure out whether we are client or server, and get default classpath elements
    accordingly.

    :param devroot the devroot parameter for Iris; will be set by the time this is called
    :param workspace the workspace parameter for Iris; will be set by the time this is called
    :return: the default classpath as an array of strings
    """

    # first determine whether this is client or server
    # clients have devroot/getdown.txt
    # servers have /usr/illumon/latest
    # if neither seems to apply, fail

    isclient = None
    if os.path.isfile("%s/getdown.txt" % devroot):
        isclient = True
    else:
        if os.path.isdir("/urs/illumon/latest"):
            isclient = False
        else:
            raise IOError("Could not decide how to create classpath. Neither /usr/illumon/latest nor devroot/getdown.txt exist")

    if isclient:
        # this construction should match the classpath specified in getdown.txt
        return flatten(["%s/private_classes" % devroot,
                        "%s/private_jars/*" % devroot,
                        "%s/override" % devroot,
                        "%s/resources" % devroot,
                        "%s/hotfixes/*" % devroot,
                        "%s/java_lib/*" % devroot])

    else: #is server
        # this construction should match the classpath specified in launch and launch_functions
        return flatten(["%s/etc" % workspace,
                        "/etc/sysconfig/illumon.d/override",
                        "/etc/sysconfig/illumon.d/resources",
                        "/etc/sysconfig/illumon.d/java_lib/*",
                        "/etc/sysconfig/illumon.d/hotfixes/*",
                        addPluginClasspaths(),
                        "%s/etc" % devroot,
                        "%s/java_lib/*" % devroot])


def addPluginClasspaths():
    new_list = []
    addGlobal(new_list, "/etc/sysconfig/illumon.d/plugins")
    addGlobal(new_list, "/etc/illumon/plugins")
    return new_list

def addGlobal(new_list, base):
    for plugin in os.listdir(base):
        for dependency in os.listdir("%s/%s/global" % base, plugin):
            new_list += "%s/%s/global/%s" % base, plugin, dependency


def expandWildcardsInList(elements):
    new_list = []
    for element in elements:
        new_list.extend(expandWildcardsInItem(element))
    return flatten(new_list)


def expandWildcardsInItem(element):
    """
    Java classpaths can include wildcards (path/* or path/*.jar), but the way we are invoking the jvm directly
    bypasses this expansion.
    This will expand a classpath element into an array of elements.

    :return: an array of all the jars matching the input wildcard, or the original string if it isn't a wildcard
    """

    if not element.endswith(("/*", "/*.jar", os.path.sep + "*", os.path.sep + "*.jar")):
        return [element]

    # extract the base - everything up to the last separator (always accept /) followed by * or *.jar
    # (group 0 = anything)[slash or path.sep]star(group 1 optional .jar)
    # backslashes in regular expressions are problematic, so convert the element to / delimiters
    try:
        base = re.search("(.*)/\*(.jar)?$", element.replace("\\", "/")).group(1)
        # expand base
        return glob("%s/*.jar" % base)
    except AttributeError:
        return [element]


def flatten(orig):
    """
    take the list foo which contains strings and lists of strings, and return
    a flat list of strings.

    :param orig: the list to flatten
    :return:
    """
    r = []
    for x in orig:
        if hasattr(x, '__iter__') and not isinstance(x, str):
            for y in flatten(x):
                r.append(y)
        else:
            r.append(x)
    return r
