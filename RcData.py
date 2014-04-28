'''
Created on Apr 25, 2014

@author: jzhang
'''

class RcObject(object):
    '''
    classdocs
    '''
    
    class RcRelation(object):
        ''''''
    
        def __init__(self):
            ''''''
            
            self.children = {}
            self.parents = {}
            self.fields = {}
            
        def addChild(self, child):
            if self.children.get(child.getName()):
                self.children[child.getName()] = child
            
        def addParent(self, parent):
            if self.parents.get(parent.getName()):
                self.parents[parent.getName()] = parent
            
        def addField(self, field):
            if self.fields.get(field.getName()):
                self.fields[field.getName()] = field
    
    ############

    def __init__(self, name):
        '''
        Constructor
        '''
        self.id = None
        self.rcName = ''
        self.type2Relation = {}
        
    def getName(self):
        return self.rcName
    
    def getTypes(self):
        return self.type2Relation.keys()
    
    def addType(self, rcType):
        if self.type2Relation[rcType]:
            self.type2Relation[rcType] = None
        
    def addChild(self, rcType, child):
        if not self.type2Relation[rcType]:
            self.type2Relation[rcType] = RcObject.RcRelation()
            
        self.type2Relation[rcType].addChild(child)
        
    def addParent(self, rcType, parent):
        if not self.type2Relation[rcType]:
            self.type2Relation[rcType] = RcObject.RcRelation()
            
        self.type2Relation[rcType].addParent(parent)
        
    def addFiled(self, rcType, field):
        if not self.type2Relation[rcType]:
            self.type2Relation[rcType] = RcObject.RcRelation()
            
        self.type2Relation[rcType].addField(field)
        
        
        
        
        
        
        
        