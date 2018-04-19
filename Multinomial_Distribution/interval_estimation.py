import numpy as np
import random
import scipy as sp
import scipy.stats
from config import num, turn, N, cv

def get_prob(num=5):
    prob_list = []
    for i in range(num-1):
        prob_list.append(random.random())
    prob_list.append(1)
    prob_list.sort()
    for i in range(num-1,0,-1):
        prob_list[i] -= prob_list[i-1]
    print("Prob Sequence : ",prob_list)
    return prob_list

def random_pick(some_list, prob):
    x = random.uniform(0,1)
    cumulative_prob=0.0
    for i in range(len(some_list)):
        cumulative_prob += prob[i]
        if x < cumulative_prob:
            flag = i
            break
    return some_list[flag] + random.random() , flag

def simulation(some_list, prob_list, samples, samples_length, N=200):
    for i in range(N):
        x, flag = random_pick(some_list, prob_list)
        samples[flag].append(x)
        samples_length[flag] += 1
    return samples, samples_length

def p_confidence_interval(n, data, confidence=0.95):  
    # compute the confidence interval of "p" with confidence probability (default 0.95)
    p = len(data)/n
    se = (p*(1-p)/n) ** 0.5
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return p-h, p+h

if  __name__ == "__main__":
    # Init prob_list and check_point list:
    some_list = [i for i in range(num+1)]
    print("List Sequence : ", some_list)
    prob_list = get_prob(num)
    print("Confidence Value:", cv, "\n")

    # Init samples and intervals:
    samples = []
    intervals = []
    samples_length = []
    for i in range(num):
        samples.append([])
        samples_length.append(0)
        intervals.append([0, 0])

    # Begin Simulating:
    for t in range(turn):
        samples, samples_length = simulation(some_list, prob_list, samples, samples_length, N)
        print("Total Number of Samples till now: " + str(N*(t+1)))
        for i in range(num):
            if len(samples[i])>0:
                intervals[i] = p_confidence_interval(N*(t+1), samples[i], cv)
                print("Generated from In Interval " + str((some_list[i],some_list[i+1])) + " :")
                print( "Samples = "+ str(samples_length[i]), ", Confidence Interval = " + str(intervals[i]), ", Confidence Interval Length = " + str(intervals[i][1] - intervals[i][0]))
        print("\n")

    
    


