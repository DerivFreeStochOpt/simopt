"""
Summary
-------
Simulate a day's worth of sales for a newsvendor under dynamic consumer substitution
"""
import numpy as np

from base import Model, Problem


class DynamNews(Model):
    """
    A model that simulates a day's worth of sales for a newsvendor
    with a Burr Type XII demand distribution. Returns the profit, after
    accounting for order costs and salvage.

    Attributes
    ----------
    name : string
        name of model
    n_rngs : int
        number of random-number generators used to run a simulation replication
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
    fixed_factors : dict
        fixed_factors of the simulation model

    See also
    --------
    base.Model
    """
    def __init__(self, fixed_factors={}):
        self.name = "DYNAMNews"
        self.n_rngs = 1
        self.n_responses = 1
        self.factors = fixed_factors
        self.specifications = {
            "num_prod": {
                "description": "Number of Products",
                "datatype": int,
                "default": 2
            },
            "num_customer": {
                "description": "Number of Customers",
                "datatype": int,
                "default": 5
            },
            "c_utility": {
                "description": "Constant of each product's utility",
                "datatype": list,
                "default": np.array((1.0, 1.0))
            },
            "mu": {
                "description": "Mu for calculating Gumbel random variable",
                "datatype": float,
                "default": 1.0
            },
            "init_level": {
                "description": "Initial inventory level",
                "datatype": list,
                "default": np.array((2, 3))
            },
            "price": {
                "description": "Price of products",
                "datatype": list,
                "default": np.array((9, 9))
            },
            "cost": {
                "description": "Cost of products",
                "datatype": list,
                "default": np.array((5, 5))
            },
        }
        self.check_factor_list = {
            "num_prod": self.check_num_prod,
            "num_customer": self.check_num_customer,
            "c_utility": self.check_c_utility,
            "mu": self.check_mu,
            "init_level": self.check_init_level,
            "price": self.check_price,
            "cost": self.check_cost
        }
        # Set factors of the simulation model.
        super().__init__(fixed_factors)

    def check_num_prod(self):
        return self.factors["num_prod"] > 0

    def check_num_customer(self):
        return self.factors["num_customer"] > 0

    def check_c_utility(self):
        return len(self.factors["c_utility"]) == self.factors["num_prod"]

    def check_init_level(self):
        return all(self.factors["init_level"] > 0) & (len(self.factors["init_level"]) == self.factors["num_prod"])

    def check_mu(self):
        return True

    def check_price(self):
        return True
    
    def check_cost(self):
        return True
    

    def check_simulatable_factors(self):
        return True

    def replicate(self, rng_list):
        """
        Simulate a single replication for the current model factors.

        Arguments
        ---------
        rng_list : list of rng.MRG32k3a objects
            rngs for model to use when simulating a replication

        Returns
        -------
        responses : dict
            performance measures of interest
            "profit" = profit in this scenario
        """
        # Designate random number generator for generating a Gumbel random variable
        Gumbel_rng = rng_list[0]
        # Compute a Gumbel rv for the utility.
        gumbel = Gumbel_rng.gumbel(self.factors["mu"] * np.euler_gamma, self.factors["mu"], size = self.factors["num_product"])
        utility = np.zeros((self.factors["num_customer"], self.factors["num_prod"] + 1))
        for j in range(self.factors["num_prod"] + 1):
            if  j == 0:
                utility[:, j] = 0
            else:
                utility[:, j] = self.factors["c_utility"][j - 1] + gumbel[j - 1]

        # Initialize inventory
        inventory = self.factors["init_level"]
        itembought = np.zeros(self.factors["num_customers"])

        # Loop through customers
        for t in range(self.factors["num_customer"]):
            instock = np.where(inventory > 0)[0]
            itembought[t] = 0
            for j in instock:
                if utility[t][j + 1] > utility[t][itembought[t]]:
                    itembought[t] = j + 1
            if itembought[t] != 0:
                inventory[itembought[t]] -= 1
                      
        # Calculate profit.
        numsold = self.factors["init_level"] - inventory
        unitprofit = self.factors["price"] - self.factors["cost"]
        profit = unitprofit * numsold


        # Compose responses and gradients.
        responses = {"profit": profit}
        gradients = {response_key:
                     {factor_key: np.nan for factor_key in self.specifications}
                     for response_key in responses
                     }
        return responses, gradients


"""
Summary
-------
Maximize the expected profit for the continuous newsvendor problem.
"""


class DynamNewsMaxProfit(Problem):
    """
    Base class to implement simulation-optimization problems.

    Attributes
    ----------
    name : string
        name of problem
    dim : int
        number of decision variables
    n_objectives : int
        number of objectives
    n_stochastic_constraints : int
        number of stochastic constraints
    minmax : tuple of int (+/- 1)
        indicator of maximization (+1) or minimization (-1) for each objective
    constraint_type : string
        description of constraints types:
            "unconstrained", "box", "deterministic", "stochastic"
    variable_type : string
        description of variable types:
            "discrete", "continuous", "mixed"
    lower_bounds : tuple
        lower bound for each decision variable
    upper_bounds : tuple
        upper bound for each decision variable
    gradient_available : bool
        indicates if gradient of objective function is available
    optimal_value : float
        optimal objective function value
    optimal_solution : tuple
        optimal solution
    model : Model object
        associated simulation model that generates replications
    model_default_factors : dict
        default values for overriding model-level default factors
    model_fixed_factors : dict
        combination of overriden model-level factors and defaults
    model_decision_factors : set of str
        set of keys for factors that are decision variables
    rng_list : list of rng.MRG32k3a objects
        list of RNGs used to generate a random initial solution
        or a random problem instance
    factors : dict
        changeable factors of the problem
            initial_solution : tuple
                default initial solution from which solvers start
            budget : int > 0
                max number of replications (fn evals) for a solver to take
    specifications : dict
        details of each factor (for GUI, data validation, and defaults)

    Arguments
    ---------
    name : str
        user-specified name for problem
    fixed_factors : dict
        dictionary of user-specified problem factors
    model_fixed factors : dict
        subset of user-specified non-decision factors to pass through to the model

    See also
    --------
    base.Problem
    """
    def __init__(self, name="DYNAMNews-1", fixed_factors={}, model_fixed_factors={}):
        self.name = name
        self.dim = 1
        self.n_objectives = 1
        self.n_stochastic_constraints = 0
        self.minmax = (1,)
        self.constraint_type = "box"
        self.variable_type = "continuous"
        self.lower_bounds = (0,)
        self.upper_bounds = (np.inf,)
        self.gradient_available = True
        self.optimal_value = None
        self.optimal_solution = (0.1878,)  # TO DO: Generalize to function of factors.
        self.model_default_factors = {
            "purchase_price": 5.0,
            "sales_price": 9.0,
            "salvage_price": 1.0,
            "Burr_c": 2.0,
            "Burr_k": 20.0
            }
        self.model_decision_factors = {"order_quantity"}
        self.factors = fixed_factors
        self.specifications = {
            "initial_solution": {
                "description": "Initial solution from which solvers start.",
                "datatype": tuple,
                "default": (0,)
            },
            "budget": {
                "description": "Max # of replications for a solver to take.",
                "datatype": int,
                "default": 1000
            }
        }
        self.check_factor_list = {
            "initial_solution": self.check_initial_solution,
            "budget": self.check_budget
        }
        super().__init__(fixed_factors, model_fixed_factors)
        # Instantiate model with fixed factors and overwritten defaults.
        self.model = DynamNews(self.model_fixed_factors)

    def vector_to_factor_dict(self, vector):
        """
        Convert a vector of variables to a dictionary with factor keys

        Arguments
        ---------
        vector : tuple
            vector of values associated with decision variables

        Returns
        -------
        factor_dict : dictionary
            dictionary with factor keys and associated values
        """
        factor_dict = {
            "order_quantity": vector[0]
        }
        return factor_dict

    def factor_dict_to_vector(self, factor_dict):
        """
        Convert a dictionary with factor keys to a vector
        of variables.

        Arguments
        ---------
        factor_dict : dictionary
            dictionary with factor keys and associated values

        Returns
        -------
        vector : tuple
            vector of values associated with decision variables
        """
        vector = (factor_dict["order_quantity"],)
        return vector

    def response_dict_to_objectives(self, response_dict):
        """
        Convert a dictionary with response keys to a vector
        of objectives.

        Arguments
        ---------
        response_dict : dictionary
            dictionary with response keys and associated values

        Returns
        -------
        objectives : tuple
            vector of objectives
        """
        objectives = (response_dict["profit"],)
        return objectives

    def response_dict_to_stoch_constraints(self, response_dict):
        """
        Convert a dictionary with response keys to a vector
        of left-hand sides of stochastic constraints: E[Y] >= 0

        Arguments
        ---------
        response_dict : dictionary
            dictionary with response keys and associated values

        Returns
        -------
        stoch_constraints : tuple
            vector of LHSs of stochastic constraint
        """
        stoch_constraints = None
        return stoch_constraints

    def deterministic_objectives_and_gradients(self, x):
        """
        Compute deterministic components of objectives for a solution `x`.

        Arguments
        ---------
        x : tuple
            vector of decision variables

        Returns
        -------
        det_objectives : tuple
            vector of deterministic components of objectives
        det_objectives_gradients : tuple
            vector of gradients of deterministic components of objectives
        """
        det_objectives = (0,)
        det_objectives_gradients = ((0,),)
        return det_objectives, det_objectives_gradients

    def deterministic_stochastic_constraints_and_gradients(self, x):
        """
        Compute deterministic components of stochastic constraints
        for a solution `x`.

        Arguments
        ---------
        x : tuple
            vector of decision variables

        Returns
        -------
        det_stoch_constraints : tuple
            vector of deterministic components of stochastic constraints
        det_stoch_constraints_gradients : tuple
            vector of gradients of deterministic components of
            stochastic constraints
        """
        det_stoch_constraints = None
        det_stoch_constraints_gradients = None
        return det_stoch_constraints, det_stoch_constraints_gradients

    def check_deterministic_constraints(self, x):
        """
        Check if a solution `x` satisfies the problem's deterministic
        constraints.

        Arguments
        ---------
        x : tuple
            vector of decision variables

        Returns
        -------
        satisfies : bool
            indicates if solution `x` satisfies the deterministic constraints.
        """
        return x[0] > 0

    def get_random_solution(self, rand_sol_rng):
        """
        Generate a random solution for starting or restarting solvers.

        Arguments
        ---------
        rand_sol_rng : rng.MRG32k3a object
            random-number generator used to sample a new random solution

        Returns
        -------
        x : tuple
            vector of decision variables
        """
        # Generate an Exponential(rate = 1) r.v.
        x = (rand_sol_rng.expovariate(1),)
        return x
