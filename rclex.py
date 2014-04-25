'''
Created on Apr 21, 2014

@author: jzhang
'''
import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

import ply.lex as lex


class RcLex(object):
    '''
    classdocs
    '''
    
    reserved = ('BEGIN', 'END', 'ACCELERATORS', 'VIRTKEY', 'ASCII', 'NOINVERT',
                'SHIFT', 'CONTROL', 'ALT', 'BITMAP', 'CURSOR', 'DIALOG', 'DIALOGEX',
                'EXSTYLE', 'CAPTION', 'CLASS', 'STYLE', 'AUTO3STATE', 'AUTOCHECKBOX',
                'AUTORADIOBUTTON', 'CHECKBOX', 'COMBOBOX', 'CTEXT', 'DEFPUSHBUTTON',
                'EDITTEXT', 'GROUPBOX', 'LISTBOX', 'LTEXT', 'PUSHBOX', 'PUSHBUTTON',
                'RADIOBUTTON', 'RTEXT', 'SCROLLBAR', 'STATE3', 'USERBUTTON', 'BEDIT',
                'HEDIT', 'IEDIT', 'FONT', 'ICON', 'LANGUAGE', 'CHARACTERISTICS',
                'VERSION', 'MENU', 'MENUEX', 'MENUITEM', 'SEPARATOR', 'POPUP', 'CHECKED',
                'GRAYED', 'HELP', 'INACTIVE', 'MENUBARBREAK', 'MENUBREAK', 'MESSAGETABLE',
                'RCDATA', 'STRINGTABLE', 'VERSIONINFO', 'FILEVERSION', 'PRODUCTVERSION',
                'FILEFLAGSMASK', 'FILEFLAGS', 'FILEOS', 'FILETYPE', 'FILESUBTYPE', 'VALUE',
                'MOVEABLE', 'FIXED', 'PURE', 'IMPURE', 'PRELOAD', 'LOADONCALL', 'DISCARDABLE',
                'NOT'
                )
    
    tokens = reserved + ('BLOCK', 'BLOCKSTRINGFILEINFO', 'BLOCKVARFILEINFO', 'NUMBER',
                         'QUOTEDSTRING', 'SIZEDSTRING', 'STRING', 'INCLUDE', 'COMMA', 'PIPE', 'CARET',
                         'AND', 'MINUS', 'PLUS', 'PERCENT', 'TIMES', 'DIVIDE', 'TILDE', 'SIZEDUNISTRING',
                         'IGNORED_TOKEN'
                        )
    
    reserved_map = {}

    def __init__(self):
        '''
        Constructor
        '''
        for r in self.reserved:
            self.reserved_map[r.upper()] = r
            
        self.rcdata_mode = 0
        
    def rcparse_rcdata(self):
        self.rcdata_mode = 1
    
    def rcparse_normal(self):
        self.rcdata_mode = 1
    
    #############################################
    
    t_ignore = r'[ \t\r]+'
    
    def t_BLOCK(self, t):
        r'BLOCK[ \t\n]*"([^\#\n]*)"'
        blockKeyWord = t.lexmatch.group(1)
        if blockKeyWord == 'StringFileInfo':
            t.type = 'BLOCKSTRINGFILEINFO'
        elif blockKeyWord == 'VarFileInfo':
            t.type = 'BLOCKVARFILEINFO'
        else:
            t.value = blockKeyWord
        return t

    def t_INCLUDE(self, t):
        r'\#include[ \t]*"[ \t]*([\w\d\.\\]+)"'
        pass
    
    def t_OTHERMACRO(self, t):
        r'\#[^\n]*'
        pass
        
    def t_NUMBER(self, t):
        r'[0-9][x0-9A-Fa-f]*L?'
        return t
        
    def t_QUOTEDSTRING(self, t):
        r'("[^\"\n]*"[ \t\n]*)+'
        if self.rcdata_mode == 1:
            t.type = 'SIZEDSTRING'
        return t
            
    def t_STRING(self, t):
        r'[A-Za-z][^ ,\t\r\n]*'
        t.type = self.reserved_map.get(t.value, "STRING")
        return t
    
    def t_BRACE(self, t):
        r'\{|\}'
        if t.value == '\{':
            t.type = 'BEGIN'
        else:
            t.type = 'END'
        return t
    
    def t_COMMENT_SINGLELINE(self, t):
        r'\/\/.*\n'
        t.lexer.lineno += t.value.count('\n')
    
    def t_COMMENT_MULTILINE(self, t):
        r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
        t.lexer.lineno += t.value.count('\n')
    
    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')
        
#     def t_IGNORE(self, t):
#         r'[ \t\r]+'
#         pass

    t_COMMA = r','
    t_PIPE = r'\|'
    t_CARET = r'\^'
    t_AND = r'&'
    t_MINUS = r'\-'
    t_PLUS = r'\+'
    t_PERCENT = r'%'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_TILDE = r'\~'
    t_EQUAL = '='
    t_OPEN_PAREN = r'\('
    t_CLOSE_PAREN = r'\)'
    
    def t_ANYONE(self, t):
        r'.'
        pass
    
    def t_error(self, t):
        print("Illegal character %s" % repr(t.value[0]))
        t.lexer.skip(1)
        
    def Test(self, data):
        lexer = lex.lex(module = self)
        lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok: 
                break
            print(tok)
        
        
if __name__ == '__main__':
    
    rcfile = open('test.rc')
    try:
        rcdata = rcfile.read()
    finally:
        rcfile.close()
        
    rclexer = RcLex()
    rclexer.Test(rcdata)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        