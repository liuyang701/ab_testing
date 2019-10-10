import math
import numpy as np
from scipy.stats import norm


def get_sample_size_proportion(alpha, power, delta, prop1, equal_variance=False, is_two_sided=True, r=1.0):
    """
    to calculate the minimum sample size requirement for AB testing with binomial metrics (click-through rate
    /probability)
    :param equal_variance:
    :param alpha: significance level
    :param power: 1-beta error, the power of test
    :param delta: minimum detectable effect, absolute value
    :param r: ratio between experiment sample size and control sample size
    :param prop1: baseline proportion, e.g. click-through rate
    :param is_two_sided:
    :return: a tuple with minimum sample sizes for control and experiment groups
    """
    prop2 = prop1 + delta
    if is_two_sided is True:
        alpha = alpha/2
    z_alpha = norm.ppf(1-alpha)
    z_beta = norm.ppf(power)
    SEpool = abs(delta)/(z_alpha+z_beta)
    if equal_variance is True:
        p_pool = (prop1 + r*prop2)/(1+r)
        Ncon = (1-p_pool)*p_pool*(1+1/r)/SEpool**2
    else:
        Ncon = ((1-prop1)*prop1 + (1-prop2)*prop2/r)/SEpool**2
    Nexp = r*Ncon
    return math.ceil(Ncon), math.ceil(Nexp)


def get_sample_size_mean(alpha, power, delta, std=None,   is_two_sided=True, r=1.0):
    """
    to get minimum sample size for AB test with metric of mean
    estimate delta variance with historical sample sizes
    assume equal variance of control and experiment groups and estimate variance with sample standard deviation
    :param alpha: significance level
    :param power: 1-beta error
    :param delta: minimum detectable effect, absolute value
    :param std: standard deviation of historical sample data
    :param is_two_sided:
    :param r:
    :return:
    """
    if is_two_sided is True:
        alpha = alpha / 2
    z_alpha = norm.ppf(1 - alpha)
    z_beta = norm.ppf(power)
    SEpool = abs(delta) / (z_alpha + z_beta)

    if std is None:
        print('please provide "sample standard deviation"')

    Ncon = std**2*(1+1/r)/SEpool**2
    Nexp = r * Ncon
    return math.ceil(Ncon), math.ceil(Nexp)


def get_sample_size_emp_var(alpha, power, delta, delta_se, num1_aa, num2_aa, is_two_sided=True):
    """
    to get minimum sample size for AB test with any metric, regardless of the distribution
    the variance of delta can be provided analytically (if possible) or empirically (from an AA test with equal sizes)
    this function assume equal sample sizes are needed for control group and experiment group
    :param num1_aa: number of data points in group1 of A/A test
    :param num2_aa: number of data points in group2 of A/A test, num1_aa and num2_aa need to be close
    :param alpha: significance level
    :param power: 1-beta error
    :param delta: minimum detectable effect, absolute value
    :param delta_se: empirical standard error of deltas from equal sized A/A test
    :param is_two_sided:
    :return: a tuple with min num of control group and min num of experiment group
    """
    if is_two_sided is True:
        alpha = alpha / 2
    z_alpha = norm.ppf(1 - alpha)
    z_beta = norm.ppf(power)
    SEpool = abs(delta) / (z_alpha + z_beta)

    Ncon = delta_se**2 * 2 / (1/num1_aa + 1/num2_aa) / SEpool ** 2
    Nexp = Ncon
    return math.ceil(Ncon), math.ceil(Nexp)


def main():
    # get alpha
    while True:
        try:
            alpha = float(input("What is your significance level (e.g. 0.05, 0.01)?\n"))
        except ValueError:
            print("Sorry, I didn't understand that.\n")
        else:
            break

    # get power
    while True:
        try:
            power = float(input("What is your power (e.g. 0.8)?\n"))
        except ValueError:
            print("Sorry, I didn't understand that.\n")
        else:
            break

    # get whether two-sided or one-sided experiment
    while True:
        two_sided = input("Is your experiment one-sided or two-sided? \n"
                          "choose 1=one-sided, 2=two-sided\n")
        if two_sided in ["1", "2"]:
            if two_sided == "1":
                two_sided = False
            else:
                two_sided = True
            break
        else:
            print("Sorry, I didn't understand that. Please enter 1, 2 or 3\n")

    # get expected delta and variance
    while True:
        option = input("Is your metric proportion (e.g. click-through rate) or mean(e.g. average expense)? \n"
                               "choose 1=proportion, 2=mean, 3=other\n")
        if option in ["1", "2", "3"]:
            break
        else:
            print("Sorry, I didn't understand that. Please enter 1, 2 or 3\n")

    if option == "1":
        while True:
            try:
                baseline = float(input("What is your baseline?\n"))
            except ValueError:
                print("Sorry, I didn't understand that.\n")
            else:
                break

        while True:
            try:
                delta = float(input("What is your minimum detectable effect?\n"))
            except ValueError:
                print("Sorry, I didn't understand that.\n")
            else:
                break

        while True:
            try:
                ratio = float(input("What is the ratio between experiment group : control group?\n"))
            except ValueError:
                print("Sorry, I didn't understand that.\n")
            else:
                break

        result = get_sample_size_proportion(alpha, power, delta, prop1=baseline, is_two_sided=two_sided, r=ratio)

    elif option == "2":
        while True:
            try:
                std = float(input("Please provide sample standard deviation\n"))
            except ValueError:
                print("Sorry, I didn't get that.\n")

            else:
                break

        while True:
            try:
                delta = float(input("What is your minimum detectable effect?\n"))
            except ValueError:
                print("Sorry, I didn't understand that.\n")
            else:
                break

        while True:
            try:
                ratio = float(input("What is the ratio between experiment group : control group?\n"))
            except ValueError:
                print("Sorry, I didn't understand that.\n")
            else:
                break

        result = get_sample_size_mean(alpha, power, delta=delta, std=std, is_two_sided=two_sided, r=ratio)
    else:
        while True:
            try:
                delta = float(input("What is your minimum detectable effect?\n"))
            except ValueError:
                print("Sorry, I didn't understand that.\n")
            else:
                break

        while True:
            try:
                se = float(input("Please provide empirical standard error of mean difference from AA test\n"))
            except ValueError:
                print("Sorry, I didn't get that.\n")

            else:
                break

        while True:
            try:
                num1 = int(input("Please provide number of data points in group 1 of AA test\n"))
            except ValueError:
                print("Sorry, I didn't get that.\n")

            else:
                break

        while True:
            try:
                num2 = int(input("Please provide number of data points in group 2 of AA test\n"))
            except ValueError:
                print("Sorry, I didn't get that.\n")

            else:
                break

        result = get_sample_size_emp_var(alpha, power, delta=delta, delta_se=se, num1_aa=num1, num2_aa=num2,
                                         is_two_sided=two_sided)

    print("You will need: \ncontrol group:{} \nexperiment group:{}\n".format(result[0], result[1]))


if __name__ == '__main__':
    # # test
    # sizes = get_sample_size_proportion(0.05, 0.8, 0.05, 0.20, is_two_sided=True, equal_variance=True)
    # print(sizes)
    # sizes = get_sample_size_mean(0.05, 0.8, 0.025, std=0.1,
    #                              is_two_sided=True)
    # print(sizes)
    main()
