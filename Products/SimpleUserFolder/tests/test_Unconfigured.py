# Copyright (c) 2004-2006 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from base import UsageBase
from unittest import makeSuite

from Products.SimpleUserFolder.SimpleUserFolder import UnconfiguredException

class Tests(UsageBase):

    def _setup(self):
        pass
    
    def test_getUser(self):
        self.assertEqual(self.suf.getUser('test'),None)
    
    def test_getUserWithExtras(self):
        # This test becomes as above for unconfigured SUF's
        self.test_getUser()
        
    def test_getUserNames(self):
        self.assertEqual(self.suf.getUserNames(),[])

    def test_getUsers(self):
        users = self.suf.getUsers()
        self.assertEqual([user.getUserName() for user in users],
                         [])
        
    def test__doAddUser(self):
        self.assertRaises(UnconfiguredException,
                          self.suf._doAddUser,
                          'testname',
                          'testpassword',
                          [], # roles
                          '', # domains
                          )

    def test__doAddUserDuplicate(self):
        # if test__doAddUser passes, then we're fine
        self.test__doAddUser()

    def test__doChangeUser(self):        
        self.assertRaises(UnconfiguredException,
                          self.suf._doChangeUser,
                          'testname',
                          'newpassword',
                          ['some','roles'], # roles
                          '', # domains
                          )

    def test__doChangeUserSamePassword(self):        
        self.assertRaises(UnconfiguredException,
                          self.suf._doChangeUser,
                          'testname',
                          None,
                          [], # roles
                          '', # domains
                          )

    def test__doDelUsers(self):        
        self.assertRaises(UnconfiguredException,
                          self.suf._doDelUsers,
                          ['test_user'])

def test_suite():
    return makeSuite(Tests)
