# Copyright (c) 2004-2006 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from SimpleUserFolder import SimpleUserFolder
from SimpleUserFolder import addSimpleUserFolder

def initialize( context ):
    context.registerClass(SimpleUserFolder,
                          constructors=(addSimpleUserFolder,),
                          icon='www/suf.gif')
