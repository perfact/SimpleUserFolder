# Copyright (c) 2004-2006 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from base import UsageBase
from logging import getLogger
from Products.SimpleUserFolder.SimpleUserFolder import SimpleUserFolder
from unittest import makeSuite

# specific b0rking exceptions
class BorkedAddUser (Exception) : pass
class BorkedEditUser (Exception) : pass
class BorkedDeleteUser (Exception) : pass
class BorkedGetUserIds (Exception) : pass
class BorkedGetUserDetails (Exception) : pass

# a b0rked SUF
class BrokenSUF(SimpleUserFolder):

    def addUser(self,name, password, roles):
        """add a user"""
        raise BorkedAddUser

    def editUser(self,name, password, roles):
        """edit a user"""
        raise BorkedEditUser
    
    def getUserIds(self):
        """return a list of usernames"""
        raise BorkedGetUserIds

    def getUserDetails(self,name):
        """return a dictionary for the specified user"""
        raise BorkedGetUserDetails

    def deleteUser(self,name):
        """delete the specified user"""
        raise BorkedDeleteUser

class Tests(UsageBase):

    def _setup(self):
        ob =BrokenSUF()
        self.folder.manage_delObjects(ids=['acl_users'])
        self.folder._setObject('acl_users', ob)
        self.suf = self.users = self.folder.acl_users
        getLogger('event.SimpleUserFolder').disabled = True
    
    def tearDown(self):
        getLogger('event.SimpleUserFolder').disabled = 0
        UsageBase.tearDown(self)

    def test_getUser(self):
        # check for non-barfage
        self.failUnless(self.suf.getUser('test') is None)

    def test_getUserWithExtras(self):
        # This test becomes the same as the above
        self.test_getUser()
        
    def test_getUserNames(self):        
        self.assertRaises(BorkedGetUserIds,
                          self.suf.getUserNames)

    def test_getUsers(self):
        self.assertRaises(BorkedGetUserIds,
                          self.suf.getUsers)
        
    def test__doAddUser(self):
        self.assertRaises(BorkedAddUser,
                          self.suf._doAddUser,
                          'testname',
                          'testpassword',
                          ['one','two'], # roles
                          [], # domains
                          )

    def test__doAddUserDuplicate(self):
        # if test__doAddUser passes, then we're fine
        self.test__doAddUser()

    def test__doChangeUser(self):        
        self.assertRaises(BorkedEditUser,
                          self.suf._doChangeUser,
                          'test_user',
                          'newpassword',
                          ['some','roles'], # roles
                          '', # domains
                          )
                          
    def test__doChangeUserSamePassword(self):        
        self.assertRaises(BorkedEditUser,
                          self.suf._doChangeUser,
                          'test_user',
                          None,
                          ['some','roles'], # roles
                          '', # domains
                          )

    def test__doDelUsers(self):        
        self.assertRaises(BorkedDeleteUser,
                          self.suf._doDelUsers,
                          ['test_user'])
    
def test_suite():
    return makeSuite(Tests)
