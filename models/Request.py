class Request(object):

    """Class defining the Request Object"""

    def __init__(self, source_lat, source_long, dest_lat, dest_long, pickup_datetime, capacity):

        self.source_lat = source_lat
        self.source_long = source_long
        self.dest_lat = dest_lat
        self.dest_long = dest_long
        self.pickup_datetime = pickup_datetime
        self.capacity = capacity

    def __str__(self):
        print([self.source_lat, self.source_long, self.dest_lat, self.dest_long])