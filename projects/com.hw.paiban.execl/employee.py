# coding=utf-8

'''

需求：
    1.定义一个员工类，员工有姓名、工号、当天上班情况 

思路：
    1.定义组类，
    2.定义员工的属性、姓名、工号、上班情况

'''


class Employee:
    '''
    
    
    date: 日期
    today_work: 工作安排 例如：处理交接、53kf
    staff: 班次，例如：白1
    '''

    date = ''
    today_work = ''
    staff = ''

    def __init__(self,Name='',ID='',groupID=''):
        self.Name = Name
        self.ID = ID
        self.groupID = groupID


    def setWork(self,work):
        self.today_work = work

    def setStaff(self,staff):
        self.staff = staff

    def setName(self,name):
        self.Name = name

    def setID(self,ID):
        self.ID = ID

    def setGroupID(self,groupID):
        self.groupID = groupID

    def setDate(self,date):
        self.date = date
