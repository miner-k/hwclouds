#coding=utf-8

'''

需求：
    1.获取排班模板中有关不同组的相关属性
    
思路：
    1.定义组类，
    2.将数据赋值为组的类。

'''

class Group:
    '''
    定义group的属性    
    
    shift :班次
    '''

    def __init__(self,groupName='',groupID='',shift={},period=''):
        self.groupName = groupName
        self.groupID = groupID
        self.shift = shift
        self.period = period

    def setGroupName(self,name):
        self.groupName = name

    def setGroupID(self, groupID):
        self.groupID = groupID



    def setShift(self, shift):
        self.shift = shift

    def setPeriod (self, period):
        self.period = period


if __name__ == '__main__':
    group3 = Group('groupName','123',{'abc':123},'1-2')
    print group3.shift


