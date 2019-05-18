"""
Construct tables ready for printing data into nice table-like output.
Nested tables, and cells containing multiple lines, are allowed!
Exports class Table()
"""


import copy
from itertools import zip_longest

__all__ = ['Table']


class _Cell:
    """
    Generates objects for the Table class. Each Table is a
    two-dimensional row containing Cell-objects.
    """

    def __init__(self, value, max_width=None, fill=None):
        """Set value and calculates the max_width and height."""
        self.value = value
        self.max_width = max_width
        self.fill = fill

    def __repr__(self):
        """Representation of this object."""
        return f'<Cell object: value=`{self.value}`>'

    def __str__(self):
        """
        Trunks the value according to the set max_width,
        and returns a string repressentation.
        """
        v = self._trunk()
        return str(v)

    def __len__(self):
        """Returns the total width of this cell (before trunking)."""
        if isinstance(self.value, Table):
            return len(self.value)
        else:
            return max(len(v) for v in str(self.value).split('\n'))

    def __iter__(self):
        """Iterate over each trunked row of cells value."""
        v = self._trunk()
        for line in str(v).split('\n'):
            yield line

    @property
    def value(self):
        if self._value is None:
            return self._fill
        else:
            return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def fill(self):
        return self._fill

    @fill.setter
    def fill(self, value):
        if value is None:
            value = ''
        self._fill = str(value)

    @property
    def max_width(self):
        return self._max_width

    @max_width.setter
    def max_width(self, value):
        """Sets the maximum width of this Cell."""
        if value is None:
            self._max_width = value
            return
        try:
            if value > 2:
                self._max_width = value
            else:
                raise ValueError('`max_width` cannot be less then 3')
        except TypeError:
            raise TypeError('`max_width` should be an integer or `None`')

    def copy(self):
        """Copies and return data from cell."""
        if isinstance(self.value, (int, float, str)):
            return _Cell(value=self.value, max_width=self.max_width)
        elif isinstance(self.value, (list, dict, tuple, object)):
            return _Cell(value=copy.deepcopy(self.value),
                         max_width=self.max_width)

    def _trunk(self):
        """
        Trunks the value in the cell before printing.
        Adds newline chars where possible.
        """
        v = self.value
        i = self.max_width
        if v is None:
            v = self.fill
        elif isinstance(v, Table):
            v.fill = self.fill
            v.max_width = i
        elif isinstance(v, list):
            v = str(v)
        elif isinstance(v, float):
            if i is not None:
                r = i - len(str(round(v))) - 2
                if r > 0:
                    v = round(v, r)
                else:
                    v = int(v)
            else:
                v = str(v)
        # If, not elif, because float still needs to be trunked!
        if isinstance(v, int) and i is not None:
            if i is not None and len(str(round(v))) > i:
                counter = 0
                while len(str(round(v))) > i - len(str(counter)) - 1:
                    v = float(v) / 10
                    counter += 1
                v = int(v)
                v = str(v) + 'e' + str(counter)
            else:
                v = str(v)

        # If, not elif,
        # Tries to devide list (containing spaces) in multiple rows
        # Also further trunks integer after 'e' if needed
        if isinstance(v, str):
            if i is not None and len(self) > i:
                # Try splitting in words first
                words = v.split(' ')
                if max(len(w) for w in words) > i:
                    # Didn't work for largest word
                    v = v[:i-2] + '..'
                else:
                    # Break into multiple lines
                    line = ''
                    length = 0
                    for w in words:
                        length += len(w) + 1
                        if length > i:
                            line += '\n'
                            length = len(w) + 1
                        line += w + ' '
                    v = line
        return v


class Table:
    """
    Construct tables ready for printing data into nice table-like output.
    Nested tables, and cells containing multiple lines, are allowed!
    properties:
        max_width       -- Maxmum width of the Table.
        fill            -- String of the default fill for empty cells.
        col_sep         -- String of the column seperator used.
        head_sep        -- String of the head/table seperator used.
        row_count       -- Returns the numbers of rows in the Table as integer.
        column_count    -- Returns the numbers of columns in the Table as
                           an integer.
    methods:
        add_head        -- Add a list of column headings to the table.
        add_row         -- Add a list of row data to the table.
        add_column      -- Add a list of column data to the table.
        remove_head     -- Add a list of column headings to the table.
        remove_row      -- Add a list of row data to the table.
        remove_column   -- Add a list of column data to the table.
        copy            -- Returns an instance Table containing specified
                           row(s) and/or column(s).
        log             -- Same as print(Table.copy(row, column)).
    """

    def __init__(self, data=None, rows=0, columns=0, max_width=None,
                 fill=None, head_sep='+=', row_sep='+-', col_sep='|'):
        """
        Keyword arguments:
            data        -- Initial data. Needs to be an iterable object of
                           iterable objects (default None).
            rows        -- Number of initial rows (default 0).
                           Creates one row if columns != 0.
            columns     -- Number of initial columns (default 0).
                           Creates one column if rows != 0.
            max_width   -- Max width of the Table for printing (default None).
            fill        -- Empty cell fill (default '').
            head_sep    -- Seperator for heading/table.
                           First char is the char at crossing of head_sep with
                           col_sep, second char is the fillchar (default '+-').
                           When one char is given, crosschar and fillchar are
                           the same.
            row_sep     -- Seperator between rows.
                           First char is the char at crossing of col_sep and
                           row_sep. Second char is the fillchar (default '+-').
                           When one char is given, crosschar and fillchar are
                           the same.
            col_sep     -- Seperator between columns (default '|').
        """
        self._head = None
        # TODO More chars for seperators?
        # TODO Row seperator?
        # Set logical args call value
        if isinstance(data, dict):
            raise TypeError('Dicts not supported as data value')
        if rows < 0:
            raise ValueError("Number of rows can't be less then zero.")
        if columns < 0:
            raise ValueError("Number of columns can't be less then zero.")
        if columns != 0 and rows == 0:
            rows = 1
        elif rows != 0 and columns == 0:
            columns = 1
        if data is None:
            self._data = [[_Cell(None) for __ in range(columns)]
                          for __ in range(rows)]
        else:
            self._data = []
            for i, row in enumerate(data):
                if i >= rows and rows != 0:
                    break
                self._data.append([])
                for j, c in enumerate(row):
                    if j >= columns and columns != 0:
                        break
                    self._data[i].append(_Cell(data[i][j]))
                while len(self._data[i]) < columns:
                    self._data[i].append(_Cell(None))
            while len(self._data) < rows:
                self.add_row()
        self.fill = fill
        self.head_sep = head_sep
        self.row_sep = row_sep
        self.col_sep = col_sep
        self.max_width = max_width

    @property
    def max_width(self):
        return self._max_width

    @max_width.setter
    def max_width(self, value):
        """Sets the max_width of the current table."""
        self._max_width = value
        W = self.column_widths
        for row in self._data:
            for v, c in zip(W, row):
                c.max_width = v

    @property
    def head_sep(self):
        return self._head_sep

    @head_sep.setter
    def head_sep(self, value):
        """Sets the head seperator string (two chars max)."""
        if not isinstance(value, str) or len(value) > 2:
            raise ValueError('Head sep needs to be a string of max two chars')
        elif len(value) == 1:
            self._head_sep = value * 2
        elif value == '':
            self._head_sep = None
        else:
            self._head_sep = value

    @property
    def row_sep(self):
        return self._row_sep

    @row_sep.setter
    def row_sep(self, value):
        """Sets the row seperator string (two chars max)."""
        if not isinstance(value, str) or len(value) > 2:
            raise ValueError('Row sep needs to be a string of max two chars')
        elif len(value) == 1:
            self._row_sep = value * 2
        elif value == '':
            self._row_sep = None
        else:
            self._row_sep = value

    @property
    def col_sep(self):
        return self._col_sep

    @col_sep.setter
    def col_sep(self, value):
        """Sets the column seperator string (one char max)."""
        if not isinstance(value, str) or len(value) > 1:
            raise ValueError('Column sep needs to be a string of one char.')
        self._col_sep = value + ' '

    @property
    def fill(self):
        return self._fill

    @fill.setter
    def fill(self, value):
        """Sets the default filling to use. Can be of any type."""
        # TODO - Resetting fill should work on all `empty` cells
        if value is None:
            value = ''
        self._fill = value
        for row in self._data:
            for cell in row:
                cell.fill = value

    @property
    def row_count(self):
        """Returns the numbers of rows in the Table as integer."""
        return len(self._data)

    @property
    def column_count(self):
        """Returns the numbers of columns in the Table as integer."""
        # Table should always contain equal length rows and head!
        if self.row_count == 0 and self._head is None:
            return 0
        elif self.row_count == 0:
            return len(self._head)
        else:
            return len(self._data[0])

    @property
    def column_widths(self):
        """Return a list of column widths."""
        M = []
        # Add head when calculating max-widths?
        if self._head is not None:
            z = zip(self._head, *self._data)
        else:
            z = zip(*self._data)
        for column in z:
            # One space extra...
            mx = max(len(c) + len(self.col_sep) - 1 for c in column)
            if mx < 3:
                M.append(3)
            else:
                M.append(mx)
        # The last column needs to be smaller
        # Only if col_sep is set
        if len(M) > 0 and M[len(M)-1] > 3:
            M[len(M)-1] -= len(self.col_sep) - 1
        if self.max_width is not None:
            # Trunk the width of each column
            # Starting with the largest column
            # Remove the seperators for the Cell's max-width
            col_max = self.max_width - len(self.col_sep) * (len(M) - 1)
            while sum(M) > col_max:
                i = M.index(max(M))
                M[i] -= 1
        return M

    def __repr__(self):
        """Representation of this object. Nr of columns and rows are added."""
        return (f'<Table object: {self.row_count} rows'
                f' and {self.column_count} columns>')

    def __str__(self):
        """
        A performance heavy operation. Returns a string representation,
        of the current table. Trunks values as needed (set by max_width).
        Also adds seperators specified by head_sep, row_sep and col_sep.
        """
        string = ''
        if self._head is not None:
            string += self._convert_row_to_string(self._head, self.col_sep)
            if self.head_sep is not None:
                sep_row = [_Cell(self.head_sep[1:] * j)
                           for j in self.column_widths]
                string += self._convert_row_to_string(sep_row, self.head_sep)
        rows = []
        for row in self._data:
            rows.append(self._convert_row_to_string(row, self.col_sep))
        if self.row_sep is not None:
            sep_row = [_Cell(self.row_sep[1:] * j)
                       for j in self.column_widths]
            sep = self._convert_row_to_string(sep_row, self.row_sep)
            string += sep.join(rows)
        else:
            string += ''.join(rows)
        return string.strip('\n')

    def __len__(self):
        """Returns the total width of the table when printed"""
        if self.column_count == 0:
            return 0
        else:
            return (sum(self.column_widths)
                    + len(self.col_sep)
                    * (self.column_count - 1))

    def _add_data(add_func):
        """
        Decorator for add_*() functions. Checks if keyword arguments are
        valid. Sets default of keyword arguments. And, in the end, makes sure
        all rows and columns in the tabel are equal in size.
        """
        if add_func.__name__ not in ('add_row', 'add_column', 'add_head'):
            raise TypeError((f'Decorator _add_data does not support '
                             f'{add_func.__name__}'))

        def wrap_add(self, *args, **kwargs):
            # TODO This is dangerous...
            # What if len(args) == 1, and 'data' in kwargs??
            if len(args) == 1:
                (kwargs['data'],) = args
            elif add_func.__name__ in ('add_row', 'add_head'):
                if len(args) == 2:
                    (kwargs['index'], kwargs['data']) = args
            elif add_func.__name__ == 'add_column':
                if len(args) == 2:
                    (kwargs['head'], kwargs['data']) = args
                elif len(args) == 3:
                    (kwargs['index'], kwargs['head'], kwargs['data']) = args
            if 'data' in kwargs and kwargs['data'] is None\
                    or 'data' not in kwargs:
                kwargs['data'] = []
            if not isinstance(kwargs['data'], (list, str)):
                raise TypeError(f"data={kwargs['data']} not supported.")
            add_func(self, **kwargs)
            if self._head is None:
                m = max(len(r) for r in self._data)
                for row in self._data:
                    while len(row) < m:
                        row.append(_Cell(None))
            else:
                m = max(len(r) for r in [self._head, *self._data])
                for row in [self._head, *self._data]:
                    while len(row) < m:
                        row.append(_Cell(None))
        return wrap_add

    @_add_data
    def add_head(self, index=None, data=None):
        """
        Add a list of column headings to the table.
        Custom decorator: @_add_data (see docstring)
        Keyword arguments:
        index   -- Index from where the data starts replacing the current head.
                   (default None: end of head)
        data    -- List containing the headings (default None).
        """
        if self._head is None:
            self._head = []
        if index is None:
            index = len(self._head)
        self._head = [*self._head[:index],
                      *[_Cell(d) for d in data],
                      *self._head[index+len(data):]]

    @_add_data
    def add_row(self, index=None, data=None):
        """
        Add a list of row data to the table.
        Custom decorator: @_add_data (see docstring)
        Keyword arguments:
        data    -- List containing cell data (default None)
        index   -- The position of the newly added row starting at 0.
                   (default None: last row)
        """
        if index is None:
            index = self.row_count
        if len(data) == 0 and self.row_count == 0:
            data.append(None)
        self._data = [*self._data[:index],
                      [_Cell(d) for d in data],
                      *self._data[index:]]

    @_add_data
    def add_column(self, index=None, head=None, data=None):
        """
        Add a list of column data to the table.
        Custom decorator: @_add_data (see docstring)
        Keyword arguments:
        data    -- List containing cell data (default None).
        head    -- The table heading of this column (default None).
        index   -- The position of the newly added column starting at 0
                   (default None: last column).
        """
        if index is None:
            index = self.column_count
        if self.row_count == 0 and len(data) == 0:
            self._data.append([])
        while len(data) > self.row_count:
            self.add_row()
        for i in range(self.row_count):
            if i < len(data):
                value = data[i]
            else:
                value = None
            self._data[i] = [*self._data[i][:index],
                             _Cell(value),
                             *self._data[i][index:]]
        if self._head is not None:
            if head is None:
                head = None
            self._head = [*self._head[:index],
                          _Cell(head),
                          *self._head[index:]]
        elif head is not None:
            self.add_head()
            self._head[index].value = head

    def _remove_data(remove_func):
        """
        Decorator for remove_*() functions. Checks if keyword arguments are
        valid. Sets default of keyword arguments.
        """
        name = remove_func.__name__
        if name not in ('remove_row', 'remove_column', 'remove_head'):
            raise TypeError(f'Decorator _add_data does not support {name}')

        def wrap_remove(self, *args, **kwargs):
            if len(args) > 0:
                index = args[0]
            elif 'index' in kwargs:
                index = kwargs['index']
            else:
                index = None
            if index is not None:
                maximum = {
                    'remove_head':
                        len(self._head) if self._head is not None
                        else 0,
                    'remove_row': self.row_count,
                    'remove_column': self.column_count
                }[name]
                if isinstance(index, int):
                    index = [index]
                if max(index) >= maximum or min(index) < 0:
                    raise ValueError(f'Index {index} out of range for {name}.')
                if isinstance(index, dict):
                    raise ValueError('Dicts not supported in {name}.')
                if isinstance(index, list):
                    index = set(index)
                kwargs['index'] = index
            remove_func(self, **kwargs)
        return wrap_remove

    @_remove_data
    def remove_head(self, index=None):
        """
        Removes range of head(s) of the table. Data is lost!
        Custom decorator: @_remove_data (see docstring)
        Keywordarguments:
        column -- Integer or range of the columnhead(s) to be removed
                  (default None: total heading removed).
        Note: index start at 0!
        """
        # Table should always contain equal length rows and head!
        # Do not shift!
        if self._head is not None:
            if index is None:
                self._head = None
            else:
                for i in index:
                    self._head[i] = _Cell(None)

    @_remove_data
    def remove_row(self, index=None, removehead=True):
        """
        Removes the row(s) of the table.
        Custom decorator: @_remove_data (see docstring)
        Keyarguments:
        index      -- Integer or range of row(s) to be removed
                      (default None: last row).
        removehead -- Boolean: remove head when there are no rows left,
                      leaving an empty table (default True).
        Note: index start at 0!
        """
        # Table should always contain equal length rows and head!
        if index is None:
            index = [self.row_count - 1]
        for r, i in enumerate(index):
            self._data = self._data[:i-r] + self._data[i-r+1:]
        if removehead and self.row_count == 0:
            self.remove_head()

    @_remove_data
    def remove_column(self, index=None, removehead=True):
        """
        Removes the column(s) of the table.
        Custom decorator: @_remove_data (see docstring)
        Keyarguments:
        index      -- Integer or range of column(s) to be removed
                      (default None: last column).
        removehead -- Boolean: if true, head is also removed.
                      If false, column still excists, but is filled
                      with the default fill value (default True).
        Note: index start at 0!
        """
        if index is None:
            index = [self.column_count - 1]
        if removehead:
            for r, i in enumerate(index):
                self._data = [row[:i-r] + row[i-r+1:] for row in self._data]
                if self._head is not None:
                    self._head = self._head[:i-r] + self._head[i-r+1:]
        else:
            for i in index:
                for row in self._data:
                    row[i] = _Cell(None)

    def copy(self, row=None, column=None):
        """
        Returns an instance of the Table containing the heading and
        Cell(s) from the current Table.
        Note: If both row and column are ommited, return an instance of
        the whole Table.
        Keyword arguments:
        row     -- Integer, range or list of the corresponding row(s)
                   (default None).
        column  -- Integer, range or list of the corresponding column(s)
                   (default None).
        Note: index start at 0!
        """
        if isinstance(row, int):
            row = [row]
        if isinstance(column, int):
            column = [column]
        if row is not None and max(row) >= self.row_count:
            raise IndexError('Exceeding max rows.\n' + repr(self))
        if column is not None and max(column) >= self.column_count:
            raise IndexError('Exceeding max columns.\n' + repr(self))
        T = Table(
                max_width=self.max_width,
                fill=self.fill,
                head_sep=self.head_sep,
                row_sep=self.row_sep,
                col_sep=self.col_sep[:1]
        )
        if row is None and column is None:
            T._data = [[c.copy() for c in row] for row in self._data]
            T._head = [h.copy() for h in self._head]
        elif row is None:
            for c in column:
                col = [r[c].copy() for r in self._data]
                head = None
                if self._head is not None:
                    head = self._head[c].copy()
                T.add_column(head=head, data=col)
        elif column is None:
            for r in row:
                T.add_row(data=[c.copy() for c in self._data[r]])
            if self._head is not None:
                T.add_head(data=[c.copy() for c in self._head])
        else:
            T._data = []
            for r in row:
                T._data.append([self._data[r][c].copy() for c in column])
            if self._head is not None:
                T.add_head(data=[self._head[c].copy() for c in column])
        return T

    def log(self, row=None, column=None):
        """
        Prints the Cell, row or column.
        Same as print(Table.copy(row, column)).
        Keyword arguments:
        row     -- Integer or range of the corresponding row(s)
                   (default None).
        column  -- Integer or range of the corresponding column(s)
                   (default None).
        Note: index start at 0!
        """
        # TODO Make logging more efficient...
        print(self.copy(row=row, column=column))

    def _convert_row_to_string(self, row, sep):
        string = ''
        for i, c in enumerate(row):
            c.fill = self.fill
            c.max_width = self.column_widths[i]
        for line in zip_longest(*row, fillvalue=''):
            for i, value in enumerate(line):
                if value is None:
                    value = self.fill
                string += value.ljust(self.column_widths[i])
                if i < len(self.column_widths) - 1:
                    string += sep
                else:
                    string += '\n'
        return string


if __name__ == '__main__':
    print('This module is supposed to be imported!')
# TODO:
# - Resetting fill should work on all `empty` cells
# - Except any data=... on add_*(), but convert too list if not a list?
# Wishlist:
# - Nested tables side by side won't line row by row... This leaves room for
#   discussion. At the end, it's a cell containing a table, not a splitted
#   cell...
# - Make logging more efficient...
# - More chars for seperators?
# - Add max height?
