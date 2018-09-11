#!/usr/bin/env python

"""
	Package for registering or unregistering COM-servers.
	
	Package helps you to register or unregister COM-servers
	that defined in python packages.
	
	Register example:
	    
	    from regcomsrv import reg
	    import sys
	    
	    # set command line attributes
	    sys.argv.clear()
	    sys.argv.append(__file__)
	    sys.argv.append("win32com.servers.dictionary")
	    sys.argv.append("DictionaryPolicy")
	    
	    reg()
		
	Unregister example:
	    
	    from regcomsrv import reg
	    import sys
	    
	    # set command line attributes
	    sys.argv.clear()
	    sys.argv.append(__file__)
	    sys.argv.append("win32com.servers.dictionary")
	    sys.argv.append("DictionaryPolicy")
	    sys.argv.append("--unregister")
	    
	    reg()
		
	Use command line (X - major version, Y - minor version):
	    py -X.Y -m regcomsrv -h
"""

# Define metadata
__version__     = "1.0.3"
__author__      = "Vladimir Saltykov"
__copyright__   = "Copyright 2018, Vladimir Saltykov"
__email__       = "vowatchka@mail.ru"
__license__     = "MIT"
__date__        = "2018-09-11"

__all__ = ["reg"]

import argparse
import win32com.server.register
import importlib
import sys

def reg():
	"""
		Register or unregister COM servers by using command line
		
		:return None:
	"""
	# create cmd parser
	parser = argparse.ArgumentParser(prog = "regcomsrv")
	
	# add args
	parser.add_argument("module", help = "Module from that the COM-servers will be imported")
	parser.add_argument("classes", nargs = "+", help = "List of classes from specified module. This classes must implements COM-servers")
	parser.add_argument("-u", "--unregister", action = "store_true", help = "For unregistering COM-servers")
	# don't delete this parameter. It's copied from function UseCommandLine defined in module win32com.server.register
	parser.add_argument("--unattended", action = "store_true", help = "See more at win32com.server.register")
	# It's copied from function UseCommandLine defined in module win32com.server.register
	parser.add_argument("--quiet", action = "store_true", help = "See more at win32com.server.register")
	# It's copied from function UseCommandLine defined in module win32com.server.register
	parser.add_argument("--debug", action = "store_true", help = "See more at win32com.server.register")
	
	# do it because function UseCommandLine from module win32com.server.register 
	# uses argument "--unregister". Short name "-u" uses only this.
	if "-u" in sys.argv:
		sys.argv[sys.argv.index("-u")] = "--unregister"
	
	# parse cmd args
	args = parser.parse_args()
	
	# import  module
	module = args.module
	m = importlib.import_module(module)
	
	# get classes from imported module
	try:
		classes = [m.__dict__[cls] for cls in args.classes]
	except KeyError as ex:
		raise AttributeError("module %r has no attribute %s" % (m.__name__, str(ex)))
	
	action = "Registering" if not args.unregister else "Unregistering"
	print("%s COM servers %s from module %s..." % (action, ", ".join([cls._reg_progid_ for cls in classes]), m.__name__))
	
	# register/unregister
	win32com.server.register.UseCommandLine(*classes)