class RangeSet:
    def __init__(self):
        self.data = []

    def data_in_range(self, time_range):
        for ranges in self.data:
            if ranges[0] < time_range[0] and time_range[1] < ranges[1]:
                return False

        return True

    def insert_data(self, time_range):
        self.data.append(time_range)
