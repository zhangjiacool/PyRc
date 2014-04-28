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
            self.hosts = {}
            
        def addChild(self, child):
            if self.children.get(child.getName()):
                self.children[child.getName()] = child
            
        def addParent(self, parent):
            if self.parents.get(parent.getName()):
                self.parents[parent.getName()] = parent
            
        def addField(self, field):
            if self.fields.get(field.getName()):
                self.fields[field.getName()] = field
                
        def addHost(self, host):
            if self.hosts.get(host.getName()):
                self.hosts[host.getName()] = host
    
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
    
    def getId(self):
        return self.id
    
    def getTypes(self):
        return self.type2Relation.keys()
    
    def addType(self, rcType):
        if self.type2Relation[rcType]:
            self.type2Relation[rcType] = RcObject.RcRelation()
        
    def addChild(self, rcType, child):
        if not self.type2Relation[rcType]:
            self.type2Relation[rcType] = RcObject.RcRelation()
        self.type2Relation[rcType].addChild(child)
        
    def addParent(self, rcType, parent):
        if not self.type2Relation[rcType]:
            self.type2Relation[rcType] = RcObject.RcRelation()
        self.type2Relation[rcType].addParent(parent)
        
    def addField(self, rcType, field):
        if not self.type2Relation[rcType]:
            self.type2Relation[rcType] = RcObject.RcRelation()
        self.type2Relation[rcType].addField(field)
        
    def addHost(self, rcType, host):
        if not self.type2Relation[rcType]:
            self.type2Relation[rcType] = RcObject.RcRelation()
        self.type2Relation[rcType].addHost(host)
        
        
class RcTree(object):
    ''''''
    def __init__(self):
        self.nameDict = {}
        
    def addObject(self, obj):
        if not self.nameDict[obj.getName()]:
            self.nameDict[obj.getName()] = obj
            
    def addObj(self, rcName, rcType):
        obj = self.nameDict[rcName]
        if not obj:
            obj = RcObject(rcName)
            self.nameDict[obj.getName()] = obj
        obj.addType(rcType)
        return obj
            
    def getObject(self, rcName):
        return self.nameDict[rcName]
    
                
            
        
        
        
        
        
        
        