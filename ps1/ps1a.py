# Problem Set 1A
# Author: Mykyta Horovoi
# Collaborators: None

# Part A: House Hunting

def calc_months(annual_salary = None, portion_saved = None, total_cost = None, portion_down_payment = 0.25, r = 0.04, montly_salary = 0, start_savings = 0, months = 0):
    
    annual_salary = int(input('Enter your annual salary:'))
    portion_saved = float(input('Enter the percent of your salary to save, as a decimal:'))
    total_cost = int(input('Enter the cost of your dream home:'))
    montly_salary = annual_salary/12

    current_savings = start_savings

    while current_savings < total_cost*portion_down_payment:
        current_savings += portion_saved*montly_salary + current_savings*r/12
        months += 1
    return print(f"Your annual salary: {annual_salary}.\nThe percent of your salary to save, as a decimal: {portion_saved}.\nThe cost of your dream home: {total_cost}.\nNumber of months: {months}.")

# Test the function
if __name__ == "__main__":
    
    # Test case 1
    # annual_salary = $120 000
    # portion_saved = 0.1
    # total_cost = $1 000 000
    
    # Expected output:
    # Your annual salary: 120000.
    # The percent of your salary to save, as a decimal: 0.1.
    # The cost of your dream home: 1000000.
    # Number of months: 183.

    calc_months()