# Copyright (c) 2004-2006 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from base import UsageBase
from unittest import makeSuite
from dummyUserSource import dummyUserFolder

class Tests(UsageBase):

    def _setup(self):
        ob=dummyUserFolder()
        self.folder.manage_delObjects(ids=['acl_users'])
        self.folder._setObject('acl_users', ob)
        self.suf = self.users = self.folder.acl_users

    def _addOneWithExtras(self,username,password,roles,extra):
        # this method needs to make sure a user is available
        # called 'test_user_with_extras'
        # See test_getUserWithExtras for details
        self.suf._addOneWithExtras(username,password,roles,extra)

    def test_correctUF(self):
        # test we really have a dummyUserFolder
        assert isinstance(self.suf,dummyUserFolder)
        assert isinstance(self.folder.acl_users,dummyUserFolder)

def test_suite():
    return makeSuite(Tests)
