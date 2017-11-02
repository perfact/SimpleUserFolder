# Copyright (c) 2004-2006 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from base import UsageBase, test_dir
from unittest import makeSuite

from Products.PythonScripts.PythonScript import manage_addPythonScript

def addPythonScript(obj,id):
    f=open(test_dir+'/'+id+'.pys')     
    file=f.read()     
    f.close()     
    manage_addPythonScript(obj,id)
    obj._getOb(id).write(file)
    return getattr(obj,id)     

class Tests(UsageBase):

    def _setup(self,f=None):

        if f is None:
            f = self.folder
        # config
        addPythonScript(f,'addUser')
        addPythonScript(f,'deleteUser')
        addPythonScript(f,'editUser')
        addPythonScript(f,'getUserDetails')
        addPythonScript(f,'getUserIds')
        self.users = f
        
        # initial users
        f.addUser('test_user', 'password',['role'])

        username = 'test_user_with_extras'
        f.manage_addDTMLDocument(id=username,title='')
        user = getattr(f,username)
        user.manage_addProperty('password','password','string')
        user.manage_addProperty('roles',[],'lines')
        user.extra = {'extra1':'extra1value',
                      'extra2':2}
        
def test_suite():
    return makeSuite(Tests)
