def table_it(aList):
    # Maximum number of columns
    mostColumns = len(aList)

    # Maximum number of rows
    mostRows = 0
    for i in range(mostColumns):
        if len(aList[i]) > mostRows:
            mostRows = len(aList[i])

    # Width of each column
    columnWidths = []
    for columnIndex in range(mostColumns):
        widestRow = 0
        for rowIndex in range(len(aList[columnIndex])):
            rowWidth = len(str(aList[columnIndex][rowIndex]))
            if rowWidth > widestRow:
                widestRow = rowWidth
        columnWidths.append(widestRow)

    # Print top line
    for i in range(mostColumns):
        print(('—' * 11), end='')
        if columnWidths[i] > 10:
            print('—' * (columnWidths[i] - 8), end='')
    print('—')
    item = 0

    # Print the rest
    for i in range(mostRows):
        if i == 0:
            print('|', end='')
        else:
            print('\n|', end='')

        for j in range(mostColumns):
            if columnWidths[j] > 10:
                print((' ' * (columnWidths[j] + 2) + '|'), end='')
            else:
                print((' ' * 10 + '|'), end='')

        print('\n|', end='')

        for ii in range(mostColumns):
            try:
                if columnWidths[ii] > 10:
                    print(str(aList[ii][item]).center(columnWidths[ii] + 2, ' ') + '|', end='')
                else:
                    print(str(aList[ii][item]).center(10, ' ') + '|', end='')

            except IndexError:
                if columnWidths[ii] > 10:
                    print(' ' * (columnWidths[ii] + 2) + '|', end='')
                else:
                    print(' ' * 10 + '|', end='')

        print('\n|', end='')

        for j in range(mostColumns):
            if columnWidths[j] > 10:
                print((' ' * (columnWidths[j] + 2) + '|'), end='')
            else:
                print((' ' * 10 + '|'), end='')

        print('\n', end='')

        # Print bottom line
        for k in range(mostColumns):
            print(('—' * 11), end='')
            if columnWidths[k] > 10:
                print('—' * (columnWidths[k] - 8), end='')
        item += 1
        print('—', end='')
    print()
