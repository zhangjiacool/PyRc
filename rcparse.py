'''
Created on Apr 21, 2014

@author: jzhang
'''
import rclex
import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

import ply.yacc as yacc
import RcData.RcTree as RcTree
import RcData.RcObject as RcObject
import RcData.Pair as Pair

rc_accelerator = "ACCELERATOR"
rc_accelerators = "ACCELERATORS"
rc_bitmp = 'BITMAP'
rc_cursor = 'CURSOR'
rc_dialog = 'DIALOG'

class RcParse(object):
    '''
    classdocs
    '''  
    tokens = rclex.RcLex.tokens
    
    precedence = (
               ('left', 'PIPE'),
               ('left', 'CARET'),
               ('left', 'AND'),
               ('left', 'PLUS', 'MINUS'),
               ('left', 'TIMES', 'DIVIDE', 'PERCENT'),
               ('right','TILDE', 'NEG')
               )


    def __init__(self):
        '''
        Constructor
        '''
        self.rcTree = RcTree()
        
    def addObj(self, rcName, rcType):
        return self.rcTree.addObj(rcName, rcType)
        
    ###############################
    
    def p_input(self, p):
        '''input : empty
                 | input accelerator
                 | input bitmap
                 | input cursor
                 | input dialog
                 | input font
                 | input icon
                 | input language
                 | input menu
                 | input menuex
                 | input messagetable
                 | input stringtable
                 | input toolbar
                 | input user
                 | input versioninfo
                 | input IGNORED_TOKEN
        '''
        pass
        
    def p_empty(self, p):
        '''empty : '''
        p[0] = None
    
    #Accelerator resources.
    def p_accelerator(self, p):
        '''accelerator : id ACCELERATORS suboptions BEG acc_entries END'''
        p[0] = self.addObj(p[1], rc_accelerators)
        for acc in p[5]:
            if acc:
                acc.addParent(rc_accelerators, p[0])
                p[0].addChild(acc.first, acc.second)
  
    def p_acc_entries(self, p):
        '''acc_entries : empty
                       | acc_entries acc_entry'''
        if p[1]:
            p[0] = p[1].append(p[2])
        else:
            p[0] = []
        
    def p_acc_entry(self, p):
        '''acc_entry : acc_event COMMA id
                     | acc_event COMMA id COMMA acc_options'''
        p[0] = Pair(rc_accelerator, self.addObj(p[3], rc_accelerator))
    
    def p_acc_event(self, p):
        '''acc_event : QUOTEDSTRING
                     | posnumexpr'''
        pass
    
    def p_acc_options(self, p):
        '''acc_options : acc_option
                       | acc_options COMMA acc_option
                       | acc_options acc_option'''
        pass
    
    def p_acc_option(self, p):
        '''acc_option : VIRTKEY
                      | ASCII
                      | NOINVERT
                      | SHIFT
                      | CONTROL
                      | ALT'''
        pass
                    
    #Bitmap resources.
    
    def p_bitmap(self, p):
        '''bitmap : id BITMAP memflags_move file_name'''
        p[0] = self.addObj(p[1], rc_bitmp)
    
    #Cursor resources.
    
    def p_cursor(self, p):
        '''cursor : id CURSOR memflags_move_discard file_name'''
        p[0] = self.addObj(p[1], rc_cursor)
    
    #Dialog resources.
    
    def p_dialog(self, p):
        '''dialog : id DIALOG memflags_move exstyle posnumexpr cnumexpr cnumexpr cnumexpr styles BEG controls END
                  | id DIALOGEX memflags_move exstyle posnumexpr cnumexpr cnumexpr cnumexpr styles BEG controls END
                  | id DIALOGEX memflags_move exstyle posnumexpr cnumexpr cnumexpr cnumexpr cnumexpr styles BEG controls END'''
        if len(p) == 13:
            idx = 11
        else:
            idx = 12
        p[0] = self.addObj(p[1], rc_dialog)
        for acc in p[idx]:
            if acc:
                acc.addParent(rc_dialog, p[0])
                p[0].addChild(acc.first, acc.second)
    
    def p_exstyle(self, p):
        '''exstyle : empty
                   | EXSTYLE EQUAL numexpr'''
        pass
    
    def p_styles(self, p):
        '''styles : empty
                  | styles CAPTION res_unicode_string_concat
                  | styles CLASS id
                  | styles STYLE
                  | styles EXSTYLE numexpr
                  | styles CLASS res_unicode_string_concat
                  | styles FONT numexpr COMMA res_unicode_string_concat
                  | styles FONT numexpr COMMA res_unicode_string_concat cnumexpr
                  | styles FONT numexpr COMMA res_unicode_string_concat cnumexpr cnumexpr
                  | styles FONT numexpr COMMA res_unicode_string_concat cnumexpr cnumexpr cnumexpr
                  | styles MENU id
                  | styles CHARACTERISTICS numexpr
                  | styles LANGUAGE numexpr cnumexpr
                  | styles VERSIONK numexpr'''
        pass
    
    def p_controls(self, p):
        '''controls : empty
                    | controls control'''
        if p[1]:
            p[0] = p[1].append(p[2])
        else:
            p[0] = []
    
    def p_control(self, p):
        '''control : AUTO3STATE optresidc
                   | AUTOCHECKBOX optresidc
                   | AUTORADIOBUTTON optresidc
                   | BEDIT optresidc control_params
                   | CHECKBOX optresidc control_params
                   | COMBOBOX control_params
                   | CONTROL optresidc numexpr cresid control_styleexpr cnumexpr cnumexpr cnumexpr cnumexpr optcnumexpr opt_control_data
                   | CONTROL optresidc numexpr cresid control_styleexpr cnumexpr cnumexpr cnumexpr cnumexpr cnumexpr cnumexpr opt_control_data
                   | CTEXT optresidc control_params
                   | DEFPUSHBUTTON optresidc control_params
                   | EDITTEXT control_params
                   | GROUPBOX optresidc
                   | HEDIT optresidc control_params
                   | ICON resref numexpr cnumexpr cnumexpr opt_control_data
                   | ICON resref numexpr cnumexpr cnumexpr cnumexpr cnumexpr
                   | ICON resref numexpr cnumexpr cnumexpr cnumexpr cnumexpr
                   | ICON resref numexpr cnumexpr cnumexpr cnumexpr cnumexpr icon_styleexpr cnumexpr cnumexpr opt_control_data
                   | IEDIT optresidc control_params
                   | LISTBOX control_params
                   | LTEXT optresidc control_params
                   | PUSHBOX optresidc control_params
                   | PUSHBUTTON optresidc control_params
                   | RADIOBUTTON optresidc control_params
                   | RTEXT optresidc control_params
                   | SCROLLBAR control_params
                   | STATE3 optresidc control_params
                   | USERBUTTON resref numexpr COMMA numexpr COMMA numexpr COMMA numexpr COMMA numexpr COMMA styleexpr optcnumexpr'''
        pass
    
#     Parameters for a control.  The static variables DEFAULT_STYLE,
#     BASE_STYLE, and CLASS must be initialized before this nonterminal
#     is used.  DEFAULT_STYLE is the style to use if no style expression
#     is specified.  BASE_STYLE is the base style to use if a style
#     expression is specified; the style expression modifies the base
#     style.  CLASS is the class of the control.

    def p_control_params(self, p):
        '''control_params : numexpr cnumexpr cnumexpr cnumexpr cnumexpr opt_control_data
                          | numexpr cnumexpr cnumexpr cnumexpr cnumexpr control_params_styleexpr optcnumexpr opt_control_data
                          | numexpr cnumexpr cnumexpr cnumexpr cnumexpr'''
        pass
    
    def p_cresid(self, p):
        '''cresid : COMMA resid'''
        pass
    
    def p_optresidc(self, p):
        '''optresidc : empty
                     | resid COMMA'''
        pass
    
    def p_resid(self, p):
        '''resid : posnumexpr
                 | res_unicode_string_concat'''
        pass
    
    def p_opt_control_data(self, p):
        '''opt_control_data : empty
                            | BEG optrcdata_data END'''
        pass
    
    #These only exist to parse a reduction out of a common case.
    
    def p_control_styleexpr(self, p):
        '''control_styleexpr : COMMA styleexpr'''
        pass
    
    def p_icon_styleexpr(self, p):
        '''icon_styleexpr : COMMA styleexpr'''
        pass
    
    def p_control_params_styleexpr(self, p):
        '''control_params_styleexpr : COMMA styleexpr'''
        pass
    
    #Font resources.
    
    def p_font(self, p):
        '''font : id FONT memflags_move_discard file_name'''
        pass
    
    #Icon resources.
    
    def p_icon(self, p):
        '''icon : id ICON memflags_move_discard file_name'''
        pass
    
#     Language command.  This changes the static variable language, which
#     affects all subsequent resources.

    def p_language(self, p):
        '''language : LANGUAGE numexpr cnumexpr'''
        pass
    
    #Menu resources.
    
    def p_menu(self, p):
        '''menu : id MENU suboptions BEG menuitems END'''
        pass
    
    def p_menuitems(self, p):
        '''menuitems : empty
                     | menuitems menuitem'''
        pass
    
    def p_menuitem(self, p):
        '''menuitem : MENUITEM res_unicode_string_concat cnumexpr menuitem_flags
                    | MENUITEM SEPARATOR
                    | POPUP res_unicode_string_concat menuitem_flags BEG menuitems END'''
        pass
    
    def p_menuitem_flags(self, p):
        '''menuitem_flags : empty
                          | menuitem_flags COMMA menuitem_flag
                          | menuitem_flags menuitem_flag'''
        pass
    
    def p_menuitem_flag(self, p):
        '''menuitem_flag : CHECKED
                         | GRAYED
                         | HELP
                         | INACTIVE
                         | MENUBARBREAK
                         | MENUBREAK'''
        pass
    
    #Menuex resources.
    
    def p_menuex(self, p):
        '''menuex : id MENUEX suboptions BEG menuexitems END'''
        pass
    
    def p_menuexitems(self, p):
        '''menuexitems : empty
                       | menuexitems menuexitem'''
        pass
    
    def p_menuexitem(self, p):
        '''menuexitem : MENUITEM res_unicode_string_concat
                      | MENUITEM res_unicode_string_concat cnumexpr
                      | MENUITEM res_unicode_string_concat cnumexpr cnumexpr optcnumexpr
                      | MENUITEM SEPARATOR
                      | POPUP res_unicode_string_concat BEG menuexitems END
                      | POPUP res_unicode_string_concat cnumexpr BEG menuexitems END
                      | POPUP res_unicode_string_concat cnumexpr cnumexpr BEG menuexitems END
                      | POPUP res_unicode_string_concat cnumexpr cnumexpr cnumexpr optcnumexpr'''
        pass
    
    #Messagetable resources.
    
    def p_messagetable(self, p):
        '''messagetable : id MESSAGETABLE memflags_move file_name'''
        pass
    
#     We use a different lexing algorithm, because rcdata strings may
#     contain embedded null bytes, and we need to know the length to use.

    def p_optrcdata_data(self, p):
        '''optrcdata_data : optrcdata_data_int'''
        pass
    
    def p_optrcdata_data_int(self, p):
        '''optrcdata_data_int : empty
                              | rcdata_data'''
        pass
    
    def p_rcdata_data(self, p):
        '''rcdata_data : sizedstring
                       | sizedunistring
                       | sizednumexpr
                       | rcdata_data COMMA sizedstring
                       | rcdata_data COMMA sizedunistring
                       | rcdata_data COMMA sizednumexpr
                       | rcdata_data COMMA'''
        pass
    
    #Stringtable resources.
    
    def p_stringtable(self, p):
        '''stringtable : STRINGTABLE suboptions BEG '''
        pass
    
    def p_string_data(self, p):
        '''string_data : empty
                       | string_data numexpr res_unicode_sizedstring_concat
                       | string_data numexpr ',' res_unicode_sizedstring_concat
                       | string_data error'''
        pass
    
    def p_rcdata_id(self, p):
        '''rcdata_id : id
                     | HTML
                     | RCDATA
                     | MANIFEST
                     | PLUGPLAY
                     | VXD
                     | DLGINCLUDE
                     | DLGINIT
                     | ANICURSOR
                     | ANIICON'''
        pass
    
#     User defined resources.  We accept general suboptions in the
#     file_name case to keep the parser happy.

    def p_user(self, p):
        '''user : id rcdata_id suboptions BEG optrcdata_data END
                | id rcdata_id suboptions file_name'''
        pass
    
    def p_toolbar(self, p):
        '''toolbar : id TOOLBAR suboptions numexpr cnumexpr BEG toolbar_data END'''
        pass
    
    def p_toolbar_data(self, p):
        '''toolbar_data : empty
                        | toolbar_data BUTTON id
                        | toolbar_data SEPARATOR'''
        pass
    
    #Versioninfo resources.
    
    def p_versioninfo(self, p):
        '''versioninfo : id VERSIONINFO fixedverinfo BEG verblocks END'''
        pass
    
    def p_fixedverinfo(self, p):
        '''fixedverinfo : empty
                        | fixedverinfo FILEVERSION numexpr optcnumexpr optcnumexpr optcnumexpr
                        | fixedverinfo PRODUCTVERSION numexpr optcnumexpr optcnumexpr optcnumexpr
                        | fixedverinfo FILEFLAGSMASK numexpr
                        | fixedverinfo FILEFLAGS numexpr
                        | fixedverinfo FILEOS numexpr
                        | fixedverinfo FILETYPE numexpr
                        | fixedverinfo FILESUBTYPE numexpr'''
        pass
    
#     To handle verblocks successfully, the lexer handles BLOCK
#     specially.  A BLOCK "StringFileInfo" is returned as
#     BLOCKSTRINGFILEINFO.  A BLOCK "VarFileInfo" is returned as
#     BLOCKVARFILEINFO.  A BLOCK with some other string returns BLOCK
#     with the string as the value.

    def p_verblocks(self, p):
        '''verblocks : empty
                     | verblocks BLOCKSTRINGFILEINFO BEG verstringtables END
                     | verblocks BLOCKVARFILEINFO BEG VALUE res_unicode_string_concat vertrans END'''
        pass
    
    def p_verstringtables(self, p):
        '''verstringtables : empty
                           | verstringtables BLOCK BEG vervals END'''
        pass
    
    def p_vervals(self, p):
        '''vervals : empty
                   | vervals VALUE res_unicode_string_concat COMMA res_unicode_string_concat'''
        pass
    
    def p_vertrans(self, p):
        '''vertrans : empty
                    | vertrans cnumexpr cnumexpr'''
        pass
    
    #A resource ID.
    
    def p_id(self, p):
        '''id : empty
              | resname'''
        pass
    
    #A resource reference.
    
    def p_resname(self, p):
        '''resname : res_unicode_string
                   | STRING
                   | NUMBER'''
        pass
    
    def p_resref(self, p):
        '''resref : posnumexpr COMMA
                  | resname
                  | resname COMMA'''
        pass
    
#     Generic suboptions.  These may appear before the BEGIN in an    y
#     multiline statement.
    def p_suboptions(self, p):
        '''suboptions : empty
                      | suboptions memflag
                      | suboptions CHARACTERISTICS numexpr
                      | suboptions LANGUAGE numexpr cnumexpr
                      | suboptions VERSIONK numexpr'''
        pass
    
    #Memory flags which default to MOVEABLE and DISCARDABLE.
    
    def p_memflags_move_discard(self, p):
        '''memflags_move_discard : empty
                                 | memflags_move_discard memflag'''
        pass
    
    #Memory flags which default to MOVEABLE.
    
    def p_memflags_move(self, p):
        '''memflags_move : empty
                         | memflags_move memflag'''
        pass
    
#     Memory flags.  This returns a struct with two integers, because we
#     sometimes want to set bits and we sometimes want to clear them.

    def p_memflag(self, p):
        '''memflag : MOVEABLE
                   | FIXED
                   | PURE
                   | IMPURE
                   | PRELOAD
                   | LOADONCALL
                   | DISCARDABLE'''
        pass
    
    #A file name.
    
    def p_file_name(self, p):
        '''file_name : QUOTEDSTRING
                     | STRING'''
        pass
    
    #Concat string
    
    def p_res_unicode_string_concat(self, p):
        '''res_unicode_string_concat : res_unicode_string
                                     | res_unicode_string_concat res_unicode_string'''
        pass
    
    def p_res_unicode_string(self, p):
        '''res_unicode_string : QUOTEDUNISTRING
                              | QUOTEDSTRING'''
        pass
    
    def p_res_unicode_sizedstring(self, p):
        '''res_unicode_sizedstring : sizedunistring
                                   | sizedstring'''
        pass
    
    #Concat string
    
    def p_res_unicode_sizedstring_concat(self, p):
        '''res_unicode_sizedstring_concat : res_unicode_sizedstring
                                        | res_unicode_sizedstring_concat res_unicode_sizedstring'''
        pass
    
    def p_sizedstring(self, p):
        '''sizedstring : SIZEDSTRING
                       | sizedstring SIZEDSTRING'''
        pass
    
    def p_sizedunistring(self, p):
        '''sizedunistring : SIZEDUNISTRING
                          | sizedunistring SIZEDUNISTRING'''
        pass
    
#     A style expression.  This changes the static variable STYLE.  We do
#     it this way because rc appears to permit a style to be set to
#     something like
#         WS_GROUP | NOT WS_TABSTOP
#     to mean that a default of WS_TABSTOP should be removed.  Anything
#     which wants to accept a style must first set STYLE to the default
#     value.  The styleexpr nonterminal will change STYLE as specified by
#     the user.  Note that we do not accept arbitrary expressions here,
#     just numbers separated by '|'.

    def p_styleexpr(self, p):
        '''styleexpr : parennumber
                     | NOT parennumber
                     | styleexpr PIPE parennumber
                     | styleexpr PIPE NOT parennumber'''
        pass
    
    def p_parennumber(self, p):
        '''parennumber : NUMBER
                       | OPEN_PAREN numexpr CLOSE_PAREN'''
        pass
    
    #An optional expression with a leading comma.
    
    def p_optcnumexpr(self, p):
        '''optcnumexpr : empty
                       | cnumexpr'''
        pass
    
    #An expression with a leading comma.
    
    def p_cnumexpr(self, p):
        '''cnumexpr : COMMA numexpr'''
        pass
    
    #A possibly negated numeric expression.
    
    def p_numexpr(self, p):
        '''numexpr : sizednumexpr'''
        pass
    
    #A possibly negated expression with a size.
    
    def p_sizednumexpr(self, p):
        '''sizednumexpr : NUMBER
                        | OPEN_PAREN sizednumexpr CLOSE_PAREN
                        | TILDE sizednumexpr %prec TILDE
                        | MINUS sizednumexpr %prec NEG
                        | sizednumexpr TIMES sizednumexpr
                        | sizednumexpr DIVIDE sizednumexpr
                        | sizednumexpr PERCENT sizednumexpr
                        | sizednumexpr PLUS sizednumexpr
                        | sizednumexpr MINUS sizednumexpr
                        | sizednumexpr AND sizednumexpr
                        | sizednumexpr CARET sizednumexpr
                        | sizednumexpr PIPE sizednumexpr'''
        pass
    
#     An expression with a leading comma which does not use unary
#     negation.

    def p_cposnumexpr(self, p):
        '''cposnumexpr : COMMA posnumexpr'''
        pass
    
    #An expression which does not use unary negation.
    
    def p_posnumexpr(self, p):
        '''posnumexpr : sizedposnumexpr'''
        pass
    
#     An expression which does not use unary negation.  We separate unary
#     negation to avoid parsing conflicts when two numeric expressions
#     appear consecutively.

    def p_sizedposnumexpr(self, p):
        '''sizedposnumexpr : NUMBER
                           | OPEN_PAREN sizednumexpr CLOSE_PAREN
                           | TILDE sizednumexpr %prec TILDE
                           | sizedposnumexpr TIMES sizednumexpr
                           | sizedposnumexpr DIVIDE sizednumexpr
                           | sizedposnumexpr PERCENT sizednumexpr
                           | sizedposnumexpr PLUS sizednumexpr
                           | sizedposnumexpr MINUS sizednumexpr
                           | sizedposnumexpr AND sizednumexpr
                           | sizedposnumexpr CARET sizednumexpr
                           | sizedposnumexpr PIPE sizednumexpr'''
        pass

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    