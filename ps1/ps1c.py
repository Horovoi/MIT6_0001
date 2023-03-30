# Problem Set 1C
# Author: Mykyta Horovoi
# Collaborators: None

# Part C: Finding the right amount to save away 

def calc_months_search(annual_salary = None, total_cost = 1000000, semi_annual_raise = 0.07, portion_down_payment = 0.25, r = 0.04, montly_salary = 0, start_savings = 0, months_limit = 36):
    
    annual_salary = int(input('Enter the starting salary:'))
    montly_salary = annual_salary/12
    current_savings = start_savings
    num_steps = 1
    low = 0.0000
    high = 1.0000
    portion_saved = (high + low)/2.0

    while abs(current_savings - total_cost*portion_down_payment) >= 100:
        current_savings = start_savings
        montly_salary = annual_salary/12

        for month in range(1, months_limit + 1):
            if month % 6 != 0 or month == 0:
                montly_salary = montly_salary
            else:
                montly_salary = montly_salary*(1 + semi_annual_raise)
            current_savings += portion_saved*montly_salary + current_savings*r/12

        if current_savings < total_cost*portion_down_payment:
            low = portion_saved
        else:
            high = portion_saved
        portion_saved = (high + low)/2.0

        num_steps += 1

        # The max amount of guesses needed is log base 2 of 10000 which is slightly above 13.
        if num_steps > 13:
            return print('It is not possible to pay the down payment in three years.')

    return print(f"Best saving rate is: {round(portion_saved, 4)}.\nSteps in bisection search: {num_steps}.")

# Test the function
if __name__ == "__main__":
    
    # Test case 1
    # annual_salary = $150 000

    # Expected output:
    # Best saving rate is: 0.4363.
    # Steps in bisection search: 12.

    # Test case 2
    # annual_salary = $10 000

    # Expected output:
    # It is not possible to pay the down payment in three years.

    calc_months_search()