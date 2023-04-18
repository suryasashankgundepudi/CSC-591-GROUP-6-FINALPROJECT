from num import NUM
from sym import SYM


class COL:

    def __init__(self, names):
        """
        Initializing function for COL class to hold column values.
        names : the names of columns
        all  : data
        x  : x val
        y : y val
        """
        self.names = names
        self.all = []
        self.klass = None
        self.x = []
        self.y = []

        for column_name in self.names:
            if column_name[0].isupper():
                column = NUM(names.index(column_name), column_name)
            else:
                column = SYM(names.index(column_name), column_name)

            if column_name[-1] != ':':
                if '!' in column_name or '+' in column_name :
                    self.y.append(column)
                else:
                    self.x.append(column)

            if column_name[-1] == '!':
                self.klass = column
            self.all.append(column)

    def __str__(self):
        """
        Function for returning all properties of the column
        """
        return f"names is {self.names}, all is {self.all}, klass is {self.klass}, x is {self.x}, y is {self.y}"

    def add(self, row):
        """
        Function for adding a new row to the column
        """
        for t in [self.x, self.y]:
            for col in t:
                col.add(row.cells[col.at])
