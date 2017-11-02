# Copyright (c) 2004-2006 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from test_PythonScriptUsage import Tests as PythonScriptTests
from unittest import makeSuite

from Products.PythonScripts.PythonScript import manage_addPythonScript

class Tests(PythonScriptTests):

    def _setup(self):
        PythonScriptTests._setup(self,self.folder.acl_users)

    def test_ReallyContains(self):
        # paranoid check that our methods are in the SUF
        # 5 methods + 2 users = 7
        self.assertEqual(len(self.suf.objectIds()),7)

def test_suite():
    return makeSuite(Tests)
