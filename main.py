import argparse
import math
import sys

parser = argparse.ArgumentParser(description="A script that takes in input flags, derives"
                                             "and calculates missing loan value")

# Adding optional arguments
parser.add_argument('--principal', type=float, help='Loan Principal')
parser.add_argument('--payment', type=float, help='Monthly payment amount')
parser.add_argument('--interest', type=float, help='Annual interest')
parser.add_argument('--periods', type=int, help='Number of periods')
parser.add_argument('--type', help='annuity or diff payment')

# Parse the arguments
args = parser.parse_args()
A = args.payment
P = args.principal
i = args.interest  # Currently yearly interest but which will be transformed to monthly interest value by dividing by 12
n = args.periods

# User must specify --type flag, otherwise program will exit
if not args.type or args.type not in ["annuity", "diff"]:
    print("Incorrect parameters")
    sys.exit()

# This is when user uses the diff mode. There are two modes the user can choose from. The "diff" and the "annuity"
# If user chooses diff, the program will figure out the payment,
# so if payment flag is provided by user, the program will exit
if args.type == "diff" and args.payment:
    print("Incorrect parameters")
    sys.exit()

# The user must provide an interest value
if not args.interest:
    print("Incorrect parameters")
    sys.exit()

# The monthly interest rate is calculated by dividing by 100 and then by 12.
# e.x.) (12 / 100) / 12 which will become 0.01 or 1%
i = args.interest = (args.interest / 100) / 12

# Here we use list comprehension to find out how many flags we received from the user
# We should have received more than 3 flags.
provided_args = sum(1 for arg in vars(args).values() if arg is not None)

# If we received less than 3 flags, program will exit.
if provided_args < 4:
    print("Incorrect parameters")
    sys.exit()

# The same is done for negative values. We should have 0 negative values.
# negative_values will become a dict, and for program to continue execution, it should be an empty dictionary
negative_values = {arg: value for arg, value in vars(args).items() if isinstance(value, (int, float)) and value < 0}

# This is when negative_values dictionary has one or more key value pair
if negative_values:
    print("Incorrect parameters")
    sys.exit()

# Finally, we check if args.type is diff to calculate the necessary values
if args.type == "diff":
    sum_paid = 0
    for k in range(1, n + 1):
        D_m = P / n + i * (P - (P * (k - 1)) / n)
        D_m = math.ceil(D_m)
        print(f"Month {k}: payment is {D_m}")
        sum_paid += D_m

    extra_paid = math.ceil(sum_paid - args.principal)
    print()
    print(f"Overpayment = {extra_paid}")
    sys.exit()


if not args.periods:
    n = args.periods = math.log(A / (A - i * P), 1+i)
    n = math.ceil(n)

    num_years = n // 12
    num_months = n % 12

    if num_years == 0:
        if num_months == 1:
            print(f"It will take {num_months} month to repay this loan!")
        else:
            print(f"It will take {num_months} months to repay this loan!")
    else:
        if num_years == 1:
            print(f"It will take {num_years} year and {num_months} months to repay this loan!")
        else:
            if num_months == 0:
                print(f"It will take {num_years} years to repay this loan!")
            else:
                print(f"It will take {num_years} years and {num_months} months to repay this loan!")

    extra_paid = math.ceil(args.payment * n - P)
    print(f"Overpayment = {extra_paid}")

if not args.payment:
    A = args.payment = math.ceil(P * (i * pow(1 + i, n)) / (pow(1 + i, n) - 1))
    print(f"Your monthly payment = {args.payment}!")
    extra_paid = math.ceil(args.payment * n - P)
    print(f"Overpayment = {extra_paid}")

if not args.principal:
    P = args.principal = round(A / ((i * pow(1 + i, n)) / (pow(1 + i, n) - 1)))
    print(f"Your loan principal = {args.principal}!")
    extra_paid = math.ceil(args.payment * n - P)
    print(f"Overpayment = {extra_paid}")
