"""
The acscteforwardmodel module contains a function `acscteforwardmodel`
that calls the ACSCTE forward model executable.
Use this function to facilitate batch runs of the forward model, or for the
TEAL interface.

Only WFC full-frame and some 2K subarrays are currently supported. See
`ACS Data Handbook <http://www.stsci.edu/hst/acs/documents/handbooks/currentDHB/>`_
for more details.

.. note:: Calibration flags are controlled by primary header.

Examples
--------

In Python without TEAL:

>>> from acstools import acscteforwardmodel
>>> acscteforwardmodel.acscteforwardmodel('*blc_tmp.fits')

In Python with TEAL:

>>> from stsci.tools import teal
>>> from acstools import acscteforwardmodel
>>> teal.teal('acscteforwardmodel')

In Pyraf::

    --> import acstools
    --> epar acscteforwardmodel

For help usage use ``exe_args=['--help']``

"""
# STDLIB
import os
import subprocess

__taskname__ = "acscteforwardmodel"
__version__ = "1.0"
__vdate__ = "19-Jul-2018"
__all__ = ['acscteforwardmodel']


def acscteforwardmodel(input, exec_path='', time_stamps=False, verbose=False,
                       quiet=False, single_core=False, exe_args=None):
    """
    Run the acscteforwardmodel.e executable as from the shell.

    Expect input to be ``*_blc_tmp.fits`` or ``*_flc.fits``.
    Output is automatically named ``*_ctefmod.fits``.

    Parameters
    ----------
    input : str or list of str
        Input filenames in one of these formats:

            * a single filename ('j1234567q_blc_tmp.fits')
            * a Python list of filenames
            * a partial filename with wildcards ('\*blc_tmp.fits')
            * filename of an ASN table ('j12345670_asn.fits')
            * an at-file (``@input``)

    exec_path : str, optional
        The complete path to ACSCTE forward model executable.
        If not given, run ACSCTE given by 'acscteforwardmodel.e'.

    time_stamps : bool, optional
        Set to True to turn on the printing of time stamps.

    verbose : bool, optional
        Set to True for verbose output.

    quiet : bool, optional
        Set to True for quiet output.

    single_core : bool, optional
        CTE correction in the ACSCTE forward model will by default try to use
        all available CPUs on your computer. Set this to True to force the use
        of just one CPU.

    exe_args : list, optional
        Arbitrary arguments passed to underlying executable call.
        Note: Implementation uses subprocess.call and whitespace is not
        permitted. E.g. use exe_args=['--nThreads', '1']

    """
    from stsci.tools import parseinput  # Optional package dependency

    if exec_path:
        if not os.path.exists(exec_path):
            raise OSError('Executable not found: ' + exec_path)
        call_list = [exec_path]
    else:
        call_list = ['acscteforwardmodel.e']

    # Parse input to get list of filenames to process.
    # acscte.e only takes 'file1,file2,...'
    infiles, dummy_out = parseinput.parseinput(input)
    call_list.append(','.join(infiles))

    if time_stamps:
        call_list.append('-t')

    if verbose:
        call_list.append('-v')

    if quiet:
        call_list.append('-q')

    if single_core:
        call_list.append('-1')

    if exe_args:
        call_list.extend(exe_args)

    subprocess.check_call(call_list)


def getHelpAsString():
    """
    Returns documentation on the `acscteforwardmodel` function.
    Required by TEAL.

    """
    return acscteforwardmodel.__doc__


def run(configobj=None):
    """
    TEAL interface for the `acscteforwardmodel` function.

    """
    acscteforwardmodel(configobj['input'],
                       exec_path=configobj['exec_path'],
                       time_stamps=configobj['time_stamps'],
                       verbose=configobj['verbose'],
                       quiet=configobj['quiet'],
                       single_core=configobj['single_core']
                       )
