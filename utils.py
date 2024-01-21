def print_chart(chart):
    for row in chart:
        for cell in row:
            print(sorted(list(cell)), end=' ')
        print()