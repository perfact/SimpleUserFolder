# Copyright (c) 2004-2010 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from AccessControl import ClassSecurityInfo
from AccessControl.SimpleObjectPolicies import _noroles
from AccessControl.class_init import InitializeClass
from AccessControl.unauthorized import Unauthorized
from OFS.ObjectManager import ObjectManager
from OFS.userfolder import BasicUserFolder
from Shared.DC.ZRDB.Results import Results
from .User import User

try:
    from Zope2.App.startup import ConflictError
except ImportError:
    # With Zope4, this changed
    from ZODB.POSException import ConflictError

import logging

ManageUsersPermission = 'Manage users'
ViewManagementPermission = 'View management screens'

logger = logging.getLogger('event.SimpleUserFolder')


def addSimpleUserFolder(self, REQUEST=None):
    """Add a SimpleUserFolder to a container as acl_users"""
    ob = SimpleUserFolder()
    self._setObject('acl_users', ob)
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)


class SimpleUserFolder(ObjectManager, BasicUserFolder):

    meta_type = "Simple User Folder"
    id = 'acl_users'
    security = ClassSecurityInfo()

    manage_options = (
        ({'label': 'Users', 'action': 'manage_main_users',
         'help': ('OFSP', 'User-Folder_Contents.stx')}, )
        + ObjectManager.manage_options[0:1]
        + BasicUserFolder.manage_options[2:]
        )

    security.declareProtected(ViewManagementPermission, 'manage_main')
    manage_main = ObjectManager.manage_main

    security.declareProtected(ManageUsersPermission, 'manage_main_users')
    manage_main_users = BasicUserFolder.manage_main

    def manage_afterAdd(self, item, container):
        ObjectManager.manage_afterAdd(self, item, container)
        BasicUserFolder.manage_afterAdd(self, item, container)

    def manage_beforeDelete(self, item, container):
        BasicUserFolder.manage_beforeDelete(self, item, container)
        ObjectManager.manage_beforeDelete(self, item, container)

    def _getMethod(self, methodName):
        # The following doesn't work at all. self.aq_parent is OK, but
        # trying to acquire the methods from another folder results in
        # a non-working environment.
        # folder = getattr(self.aq_parent, 'acl_users_d', self.aq_parent)
        folder = self
        return getattr(folder, methodName, None)

    security.declareProtected(ManageUsersPermission, 'getUserNames')

    def getUserNames(self):
        """Return a list of usernames"""
        getUserNames = self._getMethod('getUserIds')
        if getUserNames is None:
            return []
        names = getUserNames()
        if isinstance(names, Results):
            # extract names from the multiple rows returned
            names = [n.name for n in names]
        return names

    security.declareProtected(ManageUsersPermission, 'getUser')

    def getUser(self, name):
        """Return the named user object or None"""
        try:
            getUser = self._getMethod('getUserDetails')
            if getUser is None:
                return None
            user_dict = getUser(name=name)
            if not user_dict:
                return None
            if isinstance(user_dict, Results):
                result = user_dict
                user_dict = {}
                roles = []
                keys = result.names()
                row = result[0]
                for key in keys:
                    user_dict[key.lower()] = row[key]
                for row in result:
                    role = row.role
                    if role:
                        roles.append(role)
                user_dict['roles'] = roles
            user_dict['name'] = name
            u = User(user_dict)
            return u
        except Exception:
            logger.error('Error getting user %r', name,
                         exc_info=True)
            return None

    security.declareProtected(ManageUsersPermission, 'getUsers')

    def getUsers(self):
        """Return a list of user objects"""
        return list(map(self.getUser, self.getUserNames()))

    def validate(self, request, auth='', roles=_noroles):
        """
        this method performs identification, authentication, and
        authorization
        v is the object (value) we're validating access to
        n is the name used to access the object
        a is the object the object was accessed through
        c is the physical container of the object

        We allow the publishing machinery to defer to higher-level user
        folders or to raise an unauthorized by returning None from this
        method.
        """
        v = request['PUBLISHED']  # the published object
        a, c, n, v = self._getobcontext(v, request)

        # This routine is a wrapper around BasicUserFolder.validate,
        # which we call if there is no custom authorization implementation.
        getAuth = self._getMethod('getUserAuthorization')
        user = None
        if getAuth:
            auth_name, auth_password = None, None
            if auth:
                auth_name, auth_password = BasicUserFolder.identify(self, auth)
            try:
                username = getAuth(name=auth_name, password=auth_password)
            except ConflictError:
                raise
            except Exception as err:
                # raise
                logger.warn('Problem with getAuth detected!')
                logger.exception(err)
                username = None
            if username is False:
                raise Unauthorized
            if username:
                user = self.getUser(username)
        if not user:
            return None

        # The following code snippet is taken from BasicUserFolder:
        request._auth = 'basic %s:hiddenpw' % username

        # We found a user and the user wasn't the emergency user.
        # We need to authorize the user against the published object.
        if self.authorize(user, a, c, n, v, roles):
            return user.__of__(self)
        # That didn't work.  Try to authorize the anonymous user.
        elif self._isTop() and self.authorize(
                self._nobody, a, c, n, v, roles):
            return self._nobody.__of__(self)
        else:
            # we can't authorize the user, and we either can't authorize
            # nobody against the published object or we're not top-level
            return None

    def _doAddUser(self, name, password, roles, domains, **kw):
        """Create a new user. The 'password' will be the
           original input password, unencrypted. This
           method is responsible for performing any needed encryption."""

        if kw:
            raise ValueError('keyword arguments passed to _doAddUser')

        if domains:
            raise ValueError('Simple User Folder does not support domains')

        addUser = self._getMethod('addUser')
        if addUser is None:
            raise UnconfiguredException(
                'Addition of users has not been configured')

        addUser(name=name, password=password, roles=roles)

    def _doChangeUser(self, name, password, roles, domains, **kw):
        """Modify an existing user. The 'password' will be the
           original input password, unencrypted. The implementation of this
           method is responsible for performing any needed encryption."""

        if kw:
            raise ValueError('keyword arguments passed to _doChangeUser')

        if domains:
            raise ValueError('Simple User Folder does not support domains')

        changeUser = self._getMethod('editUser')
        if changeUser is None:
            raise UnconfiguredException(
                'Editing of users has not been configured')
        changeUser(name=name, password=password, roles=roles)

    def _doDelUsers(self, names):
        """Delete one or more users."""

        delUser = self._getMethod('deleteUser')
        if delUser is None:
            raise UnconfiguredException(
                'Deleting of users has not been configured')
        for name in names:
            delUser(name=name)


InitializeClass(SimpleUserFolder)


class UnconfiguredException (Exception):
    """Exception raised when a SimpleUserFolder needs configuration"""
    pass
