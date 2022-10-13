# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import grid_analyse

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # symbols = ['BTC_USD']
    symbols = ['ETH_USD']

    lst_grid_param = grid_analyse.get_grid_params(symbols, 1)

    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
