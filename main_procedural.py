import default_values
import time

power = 'on'

resources = default_values.resources.copy()
resources['money'] = 0
MENU = default_values.MENU
user_input = ''
resource_check = 1
change_sufficient = 0


def cls():
    '''scrolls screen down 100 lines'''
    print('\n'*100)


def inputs():
    '''prompts and processes all user input for coffee machine'''
    global resources
    global user_input
    print('☕')
    user_input = input('What would you like? (press "E" for espresso/"L" for latte/"C" for cappuccino(type "help" for help): ').lower()
    if user_input == 'help':
        print('FUNCTIONS: \n"off" = power off, "report" = print resources, "refill" = reset resources qty, "menu" = show menu\n'
              'COFFEE: \n"e"= espress, "c"=cappuccino, "l"=latte')
    elif user_input == 'report':
        print('report:')
        print(f'water: {resources["water"]}ml')
        print(f'milk: {resources["milk"]}ml')
        print(f'coffee: {resources["coffee"]}g')
        print(f'money: ${resources["money"]}')
    elif user_input == 'menu':
        print('MENU:')
        for key in MENU:
            print(f'{key}: ${MENU[key]["cost"]}')
    elif user_input in ('l', 'e', 'c'):
        coffee_abbreviations = {'l': 'latte', 'e': 'espresso', 'c': 'cappuccino'}
        user_input = coffee_abbreviations[user_input]
        print(f'selection: {user_input}')
    elif user_input == 'off':
        global power
        power = 'off'
    elif user_input == 'refill':
        for key in resources:
            if key in default_values.resources:
                resources[key] = default_values.resources[key]
            else:
                pass
        print('resource quantities reset to full')
    else:
        print('Input is not understood. Please try your input again')


def resource_checker():
    '''checks if ingredients are available in machine and updates resource_check variable appropriately'''
    global resource_check
    resource_check = 1
    print(f'checking machine for ingredients...')
    for key in MENU[user_input]['ingredients']:
        if resources[key] < MENU[user_input]['ingredients'][key]:
            resource_check = 0
            print(f'insufficient {key}')
    if resource_check == 1:
        print('ingredients are ready...')
    else:
        print('please fill ingredients and input "refill" to continue')


def change_intake():
    '''prompts user to input appropriate qty of money and calculates if qty is sufficient.
    displays change and updates change_sufficient variable and money resource qty appropriately '''
    print(f'please insert ${MENU[user_input]["cost"]}. Machine accepts 1s, quarters, dimes, nickels, and pennies')
    change = {'dollars':  1, 'quarters': .25, 'dimes': .1, 'nickels': .05, 'pennies': .01}
    change_total = 0
    global change_sufficient
    change_sufficient = 0
    while change_sufficient == 0:
        for key in change:
            qty = int(input(f'{key}: '))
            change_total += qty*change[key]
            print(f'amount deposited: ${change_total.__round__(2)}')
            change_return_amt = (change_total - MENU[user_input]['cost']).__round__(2)
            if change_return_amt < 0:
                print(f'amount left: ${-change_return_amt}')
                change_sufficient = 0
            else:
                change_sufficient = 1
                print(f'disbursing change: ${change_return_amt}')
                resources['money'] += MENU[user_input]['cost']
                return
        if change_sufficient == 0:
            print("Sorry that's not enough money. Money refunded.")
            return
            # dollars = input('one dollar bills: ')
            # quarters = input('quarters: ')
            # dimes = input('dimes: ')
            # nickels = input


def make_drink():
    '''lets user know drink is being made and updates ingredients availability'''
    print(f'preparing machine to make your {user_input}')
    for key in MENU[user_input]['ingredients']:
        print(f'adding {key}')
        resources[key] -= MENU[user_input]['ingredients'][key]
    print('sprinking in some love...')
    print('mixing...')
    print(f"your {user_input} is ready! Please wait 30 seconds to cool for consumption. ENJOY!")

# def coffee():
#     inputs()
#     resource_checker()


while power == 'on':
    cls()
    print(default_values.main_logo)
    inputs()
    if user_input in MENU:
        resource_checker()
        if resource_check == 1:
            change_intake()
            if change_sufficient == 1:
                make_drink()
    elif user_input == 'off':
        exit('powering off')
    time.sleep(5)