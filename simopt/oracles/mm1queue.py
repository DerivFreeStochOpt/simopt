"""
Summary
-------
Simulate a M/M/1 queue.
"""
from base import Oracle
import numpy as np

class MM1Queue(Oracle):
    """
    An oracle that simulates an M/M/1 queue with an Exponential(lambda) 
    interarrival time distribution and an Exponential(x) service time 
    distribution. Returns 
        - the average sojourn time
        - the average waiting time
        - the fraction of customers who wait
    for customers after a warmup period.

    Attributes
    ----------
    n_rngs : int
        number of random-number generators used to run a simulation replication
    rng_list : list of rng.MRG32k3a objects
        list of random-number generators used to run a simulation replication
    n_responses : int
        number of responses (performance measures)
    factors : dict
        changeable factors of the simulation model
    specifications : dict
        details of each factor (for GUI, data validation, and defaults)
    check_factor_list : dict
        switch case for checking factor simulatability

    Arguments
    ---------
    fixed_factors : nested dict
        fixed factors of the simulation model

    See also
    --------
    base.Oracle
    """
    def __init__(self, fixed_factors={}):
        self.n_rngs = 2
        self.n_responses = 2
        self.specifications = {
            "lambda": {
                "description": "Rate parameter of interarrival time distribution.",
                "datatype": float,
                "default": 1.5
            },
            "mu": {
                "description": "Rate parameter of service time distribution.",
                "datatype": float,
                "default": 3.0
            },
            "warmup": {
                "description": "Number of people as warmup before collecting statistics",
                "datatype": int,
                "default": 20
            },
            "people": {
                "description": "Number of people from which to calculate the average sojourn time",
                "datatype": int,
                "default": 50
            }
        }
        self.check_factor_list = {
            "lambda": self.check_lambda,
            "mu": self.check_mu,
            "warmup": self.check_warmup,
            "people": self.check_people
        }
        # set factors of the simulation oracle
        super().__init__(fixed_factors)

    def check_lambda(self):
        return self.factors["lambda"] > 0

    def check_mu(self):
        return self.factors["mu"] > 0

    def check_warmup(self):
        return self.factors["warmup"] >= 1

    def check_people(self):
        return self.factors["people"] >= 1

    def check_simulatable_factors(self):
        #demo for condition that queue must be stable
        #return self.factors["mu"] > self.factors["lambda"]
        return True

    def replicate(self):
        """
        Simulate a single replication for the current oracle factors.

        Returns
        -------
        responses : dict
            performance measures of interest
            "avg_sojourn_time" = average sojourn time
            "avg_waiting_time" = average waiting time
            "frac_cust_wait" = fraction of customers who wait
        gradients : dict of dicts
            gradient estimates for each response
        """
        # total number of arrivals to simulate
        total = self.factors["warmup"] + self.factors["people"]
        # designate separate random number generators
        arrival_rng = self.rng_list[0]
        service_rng = self.rng_list[1]
        # generate all interarrival times up front
        arrival_times = [arrival_rng.expovariate(self.factors["lambda"]) for _ in range(total)]
        # generate all service times up front
        service_times = [service_rng.expovariate(self.factors["mu"]) for _ in range(total)]
        # create matrix storing times and metrics for each customer
        cust_mat = np.zeros((total, 10))
        # column 0 : arrival time to queue
        cust_mat[:,0] = np.cumsum(arrival_times)
        # column 1 : service time
        cust_mat[:,1] = service_times
        # column 2 : service completion time
        # column 3 : sojourn time
        # column 4 : waiting time
        # column 5 : number of customers in system at arrival
        # column 6 : gradient of sojourn time w.r.t. mu
        # column 7 : gradient of waiting time w.r.t. mu
        # column 8 : gradient of sojourn time w.r.t. lambda
        # column 9 : gradient of waiting time w.r.t. lambda
        # input first customer times
        cust_mat[0,2] = cust_mat[0,0] + cust_mat[0,1]
        cust_mat[0,3] = cust_mat[0,1]
        cust_mat[0,4] = 0
        cust_mat[0,5] = 0
        cust_mat[0,6] = -cust_mat[0,1]/self.factors["mu"]
        cust_mat[0,7] = 0
        cust_mat[0,8] = 0
        cust_mat[0,9] = 0
        # fill in times for remaining customers
        for i in range(1,total):
            cust_mat[i,2] = max(cust_mat[i,0], cust_mat[i-1,2]) + cust_mat[i,1]
            cust_mat[i,3] = cust_mat[i,2] - cust_mat[i,0]
            cust_mat[i,4] = cust_mat[i,3] - cust_mat[i,1]
            cust_mat[i,5] = sum(cust_mat[i-int(cust_mat[i-1,5])-1:i,2] > cust_mat[i,0])
            cust_mat[i,6] = -sum(cust_mat[i-int(cust_mat[i,5]):i+1,1])/self.factors["mu"]
            cust_mat[i,7] = -sum(cust_mat[i-int(cust_mat[i,5]):i,1])/self.factors["mu"]
            cust_mat[i,8] = np.nan # ... to be derived
            cust_mat[i,9] = np.nan # ... to be derived
        # with np.printoptions(precision=3, suppress=True):
        #     print(cust_mat)    
        # compute average sojourn time and its gradient
        mean_sojourn_time = np.mean(cust_mat[self.factors["warmup"]:,3])
        grad_mean_sojourn_time_mu = np.mean(cust_mat[self.factors["warmup"]:,6])
        grad_mean_sojourn_time_lambda = np.mean(cust_mat[self.factors["warmup"]:,8])
        # compute average waiting time and its gradient
        mean_waiting_time = np.mean(cust_mat[self.factors["warmup"]:,4])
        grad_mean_waiting_time_mu = np.mean(cust_mat[self.factors["warmup"]:,7])
        grad_mean_waiting_time_lambda = np.mean(cust_mat[self.factors["warmup"]:,9])
        # compute fraction of customers who wait
        fraction_wait = np.mean(cust_mat[self.factors["warmup"]:,5] > 0)
        # compose responses
        responses = {
            "avg_sojourn_time": mean_sojourn_time,
            "avg_waiting_time": mean_waiting_time,
            "frac_cust_wait": fraction_wait
        }
        # compose gradients
        gradients = {response_key: {factor_key: np.nan for factor_key in self.specifications} for response_key in responses}
        gradients["avg_sojourn_time"]["mu"] = grad_mean_sojourn_time_mu
        gradients["avg_sojourn_time"]["lambda"] = grad_mean_sojourn_time_lambda
        gradients["avg_waiting_time"]["mu"] = grad_mean_waiting_time_mu
        gradients["avg_waiting_time"]["lambda"] = grad_mean_waiting_time_lambda
        # return responses and gradients
        return responses, gradients