# Making pretty column printed tables in Python

For some of my projects I needed support for nested tables.
I'm still learning Python, so I decided to write a module myself.

There are better tested modules on the web:
- [PrettyTable](https://pypi.org/project/PrettyTable/ "PrettyTable at pypi.org")
- [columnize](https://pypi.org/project/columnize/ "columnize at pypi.prg")
- [tabulate](https://pypi.org/project/tabulate/ "tabulate at pypi.org")

But they can't do what this baby can do ; )
Look at this awesome print!
```
A column width a Table ' Another Table
~~~~~~~~~~~~~~~~~~~~~~~x~~~~~~~~~~~~~~~~~~~~~
blk | freq | count     ' goodies
====+======+======     ' ````````````````````
ABC | 0.65 | 1337      ' newlines\n
----+------+------     ' in\n
ANR | 0.59 | 1200      ' cells\n
----+------+------     ' are\n
BJU | 0.53 | 1063      ' allowed!
----+------+------     ' ....................
CHZ | 0.47 | 926       ' long lines
----+------+------     ' get trunked
DHT | 0.41 | 789       ' automatically
----+------+------     ' when setting
EIR | 0.35 | 652       ' max_width
----+------+------     ' ....................
FKV | 0.29 | 515       ' cells can contain
----+------+------     ' any kind of object
GOZ | 0.24 | 378       ' like list, dicts
----+------+------     ' string, ints, floats
IKL | 0.18 | 241       ' and ofcourse
----+------+------     ' other Tables!
JUV | 0.12 | 104       '
---------------------------------------------
This final row is yet another Table!
```
### Goodies
+ Nested tables are allowed!
+ Newlines in a cell are allowed.
+ Tries to break a long line into multiple lines before printing.
+ Trunking also available for lists, floats, ints, and of coures tables!
+ Piping the output in terminal is possible, e.g. ... | head -10.
+ Well documented, couple of testcases added.

### Usages
1. Create a new table object:
```mytable = Table()```
2. Add rows 
```mytable.add_row(['A', 'row', 'with', 'five', 'columns'])```
   and/or columns 
```mytable.add_column(head='column', data=['A', 'column', 'with', 'five', 'rows'])```
3. Add/replace heading:
```mytable.add_head(index=0, data=['This', 'table', 'looks', 'awesome'])```
3. Customize a bit:
```T.row_sep='' T.col_sep='/' T.head_sep='o*'```
4. Print the table:
```print(mytable)```

```
This / table / looks / awesome /         / column
*****o*******o*******o*********o*********o*******
A    / row   / with  / five    / columns / A
     /       /       /         /         / column
     /       /       /         /         / with
     /       /       /         /         / five
     /       /       /         /         / rows
```

### Module info
Table()
Construct tables ready for printing data into nice table-like output.
Nested tables, and cells containing multiple lines, are allowed!

#####Object
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

#####Class

__init__

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


__repr__

    Representation of this object. Nr of columns and rows are added.

__str__

    A performance heavy operation. Returns a string representation,
    of the current table. Trunks values as needed (set by max_width).
    Also adds seperators specified by head_sep, row_sep and col_sep.

__len__

    Returns the total width of the table when printed

max_width

    Sets the max_width of the current table.

head_sep

    Sets the head seperator string (two chars max).

row_sep

    Sets the row seperator string (two chars max).

col_sep

    Sets the column seperator string (one char max).

fill

    Sets the default filling to use. Can be of any type.

row_count

    Returns the numbers of rows in the Table as integer.

column_count

    Returns the numbers of columns in the Table as integer.

column_widths

    Return a list of column widths.

add_head()

    Add a list of column headings to the table.
    Custom decorator: @_add_data (see docstring)
    Keyword arguments:
    index   -- Index from where the data starts replacing the current head.
               (default None: end of head)
    data    -- List containing the headings (default None).
    fill    -- Empty heading fill for excesive columns (default None).
               Note: if none given, the Table fill param is used!

add_row()

    Add a list of row data to the table.
    Custom decorator: @_add_data (see docstring)
    Keyword arguments:
    data    -- List containing cell data (default None)
    index   -- The position of the newly added row starting at 0.
               (default None: last row)
    fill    -- The filling too use when creating more cells to fit
               the Table size (default None)
               Noterow: If none given, the Table fill param is used!
    
add_column()

    Add a list of column data to the table.
    Custom decorator: @_add_data (see docstring)
    Keyword arguments:
    data    -- List containing cell data (default None).
    head    -- The table heading of this column (default None).
    index   -- The position of the newly added column starting at 0
               (default None: last column).
    fill    -- The filling too use when creating more cells to fit
               the Table size (default None).
               Note: If none given, the Table fill param is used!
    
remove_head()

    Removes range of head(s) of the table. Data is lost!
    Custom decorator: @_remove_data (see docstring)
    Keywordarguments:
    column -- Integer or range of the columnhead(s) to be removed
              (default None: total heading removed).
    Note: index start at 0!

remove_row()

    Removes the row(s) of the table.
    Custom decorator: @_remove_data (see docstring)
    Keyarguments:
    index      -- Integer or range of row(s) to be removed
                  (default None: last row).
    removehead -- Boolean: remove head when there are no rows left,
                  leaving an empty table (default True).
    Note: index start at 0!

remove_column()

    Removes the column(s) of the table.
    Custom decorator: @_remove_data (see docstring)
    Keyarguments:
    index      -- Integer or range of column(s) to be removed
                  (default None: last column).
    removehead -- Boolean: if true, head is also removed.
                  If false, column still excists, but is filled
                  with the default fill value (default True).
    Note: index start at 0!

copy()

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

log()

    Prints the Cell, row or column.
    Same as print(Table.copy(row, column)).
    Keyword arguments:
    row     -- Integer or range of the corresponding row(s)
               (default None).
    column  -- Integer or range of the corresponding column(s)
               (default None).
    Note: index start at 0!
    

### ToDo
- Re-setting fill should work on all `empty` cells
- Except any data=... on add_*(), but convert too list if not a list?
- Make logging more efficient...
- More/better testing

### Wishlist
- More chars for seperators?
- Add sort method?
- Cells containing functions, for calculating sum, product etc.. of range of
  Cells
- Add max height?

### Notes
- When setting max_width Table tries too shrink largest column first.
  This isn't always desirable, especially with nested tables of different
  sizes.
- Nested tables side by side won't line up row by row... This leaves room for
  discussion. At the end, it's a cell containing a table, not a splitted
  cell...
