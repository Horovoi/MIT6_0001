# Problem Set 1B
# Author: Mykyta Horovoi
# Collaborators: None

# Part B: Saving, with a raise

def calc_months_with_raise(annual_salary = None, portion_saved = None, total_cost = None, semi_annual_raise = None, portion_down_payment = 0.25, r = 0.04, montly_salary = 0, start_savings = 0, months = 0):
    
    annual_salary = int(input('Enter your annual salary:'))
    portion_saved = float(input('Enter the percent of your salary to save, as a decimal:'))
    total_cost = int(input('Enter the cost of your dream home:'))
    semi_annual_raise = float(input('Enter the semi-annual raise, as a decimal:'))
    montly_salary = annual_salary/12

    current_savings = start_savings

    while current_savings < total_cost*portion_down_payment:

        if months % 6 != 0 or months == 0:
            montly_salary = montly_salary
        else:
            montly_salary = montly_salary*(1 + semi_annual_raise)

        current_savings += portion_saved*montly_salary + current_savings*r/12
        months += 1
    return print(f"Your annual salary: {annual_salary}.\nThe percent of your salary to save, as a decimal: {portion_saved}.\nThe cost of your dream home: {total_cost}.\nThe semi-annual raise, as a decimal: {semi_annual_raise}.\nNumber of months: {months}.")

# Test the function
if __name__ == "__main__":
    
    # Test case 1
    # annual_salary = $120 000
    # portion_saved = 0.05
    # total_cost = $500 000
    # semi_annual_raise = 0.03
    
    # Expected output:
    # Your annual salary: 120000.
    # The percent of your salary to save, as a decimal: 0.05.
    # The cost of your dream home: 500000.
    # The semi-annual raise, as a decimal: 0.03.
    # Number of months: 142.

    calc_months_with_raise()