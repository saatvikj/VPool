class Vehicle(object):

    """Class defining the Vehicle Object"""

    def __init__(self, v_id, cap, cost):

        self.v_id = v_id
        self.cap = cap
        self.cost = cost
        self.passengers=[]

    def __str__(self):
        pass

    def setpass(self,paslist):
        self.passengers=paslist

    def addpass(self, v):
        self.passengers.append(v)

    def is_full(self):

        if self.cap == len(self.passengers):

            return True

        else:

            return False

def comparator(x, y):
    if(x.cost/x.cap > y.cost/y.cap):
        return 1
    elif(x.cost/x.cap == y.cost/y.cap):
        return 0
    else:
        return -1
