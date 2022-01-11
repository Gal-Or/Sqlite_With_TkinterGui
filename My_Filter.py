import re


class Filter:

    def __init__(self, attribute, operator, attr_type, value=""):
        self.attr_type = attr_type
        self.attribute = attribute
        self.operator = operator
        self.value = value
        if "IN" in operator:
            arr = re.split(' , | ,|, |,| ', value)
            arr = list(filter(lambda val: val != '', arr))
            self.value = '('
            size = len(arr)
            i = 0
            for s in arr:
                self.value += '\'' + s + '\''
                if i < size - 1:
                    self.value += ', '
                i += 1
            self.value += ')'
        elif "NVARCHAR" in attr_type and "NULL" not in operator:
            self.value = "\'" + value + "\'"
            if operator == '=':
                self.operator = 'LIKE'
            elif operator == '!=':
                self.operator = 'NOT LIKE'
            else:
                self.operator = operator
        elif "DATETIME" in attr_type:
            if operator == '=':
                self.operator = 'LIKE'
            elif operator == '!=':
                self.operator = 'NOT LIKE'
            arr = re.split('/', value)
            arr = list(filter(lambda val: val != '', arr))
            arr.reverse()
            self.value = '\''
            size = len(arr)
            i = 0
            for s in arr:
                self.value += s
                if i < size - 1:
                    self.value += '-'
                i += 1
            if operator == '=' or operator == '!=':
                self.value += '%\''
            else:
                self.value += '\''

    def __str__(self):
        return self.attribute + " " + self.operator + " " + str(self.value)
