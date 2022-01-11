

class Manager:
    """
    Singleton class
    """
    _instance: 'manager' = None

    def __init__(self):
        self.all_filters = []

    @staticmethod
    def get_instance() -> 'manager':
        """ Returns the single instance of the class or create an instance if it is the first time """
        if not Manager._instance:
            Manager._instance = Manager()

        return Manager._instance

    def add_filter(self, new_filter):
        """
        If the new filter is not exist in the filters list add it to the list.

        Parameters:
            new_filter(Filter): New filter to add.
        """
        if self.check_if_exist(new_filter) == -1:
            self.all_filters.append(new_filter)

    def check_if_exist(self, new_filter):
        """
        Checks if the new filter exist in the filters list.

        Parameters:
            new_filter(Filter): New filter to add.

        Returns:
            If exist returns the filter, else -1.
        """
        for f in self.all_filters:
            if f.attribute == new_filter.attribute and f.operator == new_filter.operator and f.value == new_filter.value:
                return self.all_filters.index(f)

        return -1

    def remove(self, f):
        """
        Checks if the new filter exist in the filters list and remove it.

        Parameters:
            f(Filter): Filter to remove.
        """
        index = self.check_if_exist(f)
        if index != -1:
            self.all_filters.remove(f)

    def __str__(self):
        str = "All Filters: \n"
        for f in self.all_filters:
            str += f.__str__() + "\n"
        return str
