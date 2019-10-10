import math
from scipy.stats import norm
import numpy as np


def signifcance_test_proportion(x_cont, n_cont, x_exp, n_exp, alpha, is_equal_var=True, is_two_sided=True):
    """
    calculate experiment effect and its confidence interval
    if 0 in the confidence interval, then no statistical significance
    :param is_equal_var: whether two groups have equal variance
    :param is_two_sided: whether the test is two-sided or one-sided
    :param x_cont: count of success in control group
    :param n_cont: count of total events in control group
    :param x_exp: count of success in experiment group
    :param n_exp: count of total events in experiment group
    :param alpha: significance level, false positive rate
    :return: difference (success rate of experiment group - success rate of control group), lower bound and upper bound
    of difference
    """
    p_cont = x_cont / n_cont
    p_exp = x_exp / n_exp
    delta = p_exp-p_cont
    if is_two_sided is True:
        alpha = alpha/2

    if is_equal_var is True:
        p_pool = (x_cont+x_exp)/(n_cont+n_exp)
        se = np.sqrt(p_pool*(1-p_pool)*(1/n_cont+1/n_exp))
    else:
        se = np.sqrt(p_cont*(1-p_cont)/n_cont+p_exp*(1-p_exp)/n_exp)

    z_alpha = norm.ppf(1-alpha)

    lower_bound = delta - z_alpha * se
    upper_bound = delta + z_alpha * se

    return round(delta, 4), round(lower_bound, 4), round(upper_bound, 4)


def main():
    # get alpha
    while True:
        try:
            alpha = float(input("What is your significance level (e.g. 0.05, 0.01)?\n"))
        except ValueError:
            print("Sorry, I didn't understand that.\n")
        else:
            break
    # get event and success counts
    while True:
        try:
            n_cont = int(input("What is the total number of events in control group?\n"))
        except ValueError:
            print("Sorry, I didn't understand that.\n")
        else:
            break

    while True:
        try:
            x_cont = int(input("What is the number of success in control group?\n"))
        except ValueError:
            print("Sorry, I didn't understand that.\n")
        else:
            break

    while True:
        try:
            n_exp = int(input("What is the total number of events in experiment group?\n"))
        except ValueError:
            print("Sorry, I didn't understand that.\n")
        else:
            break

    while True:
        try:
            x_exp = int(input("What is the number of success in experiment group?\n"))
        except ValueError:
            print("Sorry, I didn't understand that.\n")
        else:
            break

    # get whether two-sided or one-sided experiment
    while True:
        choice = input("Is your experiment one-sided or two-sided? \n"
                          "choose 1=one-sided, 2=two-sided\n")
        if choice in ["1", "2"]:
            if choice == "1":
                two_sided = False
            else:
                two_sided = True
            break
        else:
            print("Sorry, I didn't understand that. Please enter 1, 2 or 3\n")

    # get whether two groups have equal variance
    while True:
        choice = input("Is there equal variance between two groups? \n"
                          "choose 1=yes, 2=no\n")
        if choice in ["1", "2"]:
            if choice == "1":
                equal_var = True
            else:
                equal_var = False
            break
        else:
            print("Sorry, I didn't understand that. Please enter 1, 2 or 3\n")
    print((x_cont, n_cont, x_exp, n_exp, alpha, two_sided, equal_var))
    delta, lower_b, upper_b = signifcance_test_proportion(x_cont, n_cont, x_exp, n_exp, alpha,
                                                          is_two_sided=two_sided, is_equal_var=equal_var)
    print('effect size:{} , lower bound:{}, upper bound:{}'.format(delta, lower_b, upper_b))


if __name__ == '__main__':
    ## test
    # print(signifcance_test_proportion(3785, 17293, 3423, 17260, 0.05))
    # print(signifcance_test_proportion(2033, 3785, 1945, 3423, 0.05))
    # print(signifcance_test_proportion(2033, 17293, 1945, 17260, 0.05))
    main()

