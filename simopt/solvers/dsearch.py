"""
Summary
-------
Direct Search: A direct search algorithm for problems with linear constraints, i.e., Ce@x = de, Ci@x <= di.
A detailed description of the solver can be found `here <https://simopt.readthedocs.io/en/latest/pgd.html>`_.
"""
import numpy as np
import cvxpy as cp
import warnings
warnings.filterwarnings("ignore")

from ..base import Solver


class DS(Solver):
    """
    The Direct Search solver.

    Attributes
    ----------
    name : string
        name of solver
    objective_type : string
        description of objective types:
            "single" or "multi"
    constraint_type : string
        description of constraints types:
            "unconstrained", "box", "deterministic", "stochastic"
    variable_type : string
        description of variable types:
            "discrete", "continuous", "mixed"
    gradient_needed : bool
        indicates if gradient of objective function is needed
    factors : dict
        changeable factors (i.e., parameters) of the solver
    specifications : dict
        details of each factor (for GUI, data validation, and defaults)
    rng_list : list of rng.MRG32k3a objects
        list of RNGs used for the solver's internal purposes

    Arguments
    ---------
    name : str
        user-specified name for solver
    fixed_factors : dict
        fixed_factors of the solver

    See also
    --------
    base.Solver
    """
    def __init__(self, name="DS", fixed_factors={}):
        self.name = name
        self.objective_type = "single"
        self.constraint_type = "deterministic"
        self.variable_type = "continuous"
        self.gradient_needed = False
        self.specifications = {
            "crn_across_solns": {
                "description": "use CRN across solutions?",
                "datatype": bool,
                "default": True
            },
            "r": {
                "description": "number of replications taken at each solution",
                "datatype": int,
                "default": 50
            },
            "theta": {
                "description": "constant for decreasing the step size.",
                "datatype": int,
                "default": 0.2
            },
            "gamma": {
                "description": "constant for increasing the step size.",
                "datatype": int,
                "default": 2
            },
            "alpha_max": {
                "description": "maximum step size.",
                "datatype": int,
                "default": 10
            },
            "alpha_0": {
                "description": "initial step size.",
                "datatype": int,
                "default": 1
            },
            "c": {
                "description": "constant multiplier for the forcing function.",
                "datatype": float,
                "default": 1e-4
            },
            "q": {
                "description": "exponent for the forcing function.",
                "datatype": float,
                "default": 2.0
            },
            "set_size": {
                "description": "size of the set of random non-zero polling directions.",
                "datatype": int,
                "default": 10
            },
            "tol": {
                "description": "floating point comparison tolerance",
                "datatype": float,
                "default": 1e-7
            }
            
        }
        self.check_factor_list = {
            "crn_across_solns": self.check_crn_across_solns,
            "r": self.check_r,
            "theta": self.check_theta,
            "gamma": self.check_gamma,
            "alpha_max": self.check_alpha_max,
            "alpha_0": self.check_alpha_0,
            "c": self.check_c,
            "q": self.check_q,
            "set_size": self.check_set_size,
            "tol": self.check_tol,
        }
        super().__init__(fixed_factors)

    def check_r(self):
        return self.factors["r"] > 0

    def check_theta(self):
        return self.factors["theta"] > 0 & self.factors["theta"] < 1

    def check_gamma(self):
        return self.factors["gamma"] > 1

    def check_alpha_max(self):
        return self.factors["alpha_max"] > 0

    def check_alpha_0(self):
        return self.factors["alpha_0"] > 0

    def check_c(self):
        return self.factors["c"] > 0
    
    def check_q(self):
        return self.factors["q"] > 1
    
    def check_set_size(self):
        return self.factors["set_size"] >= 1

    def check_tol(self):
        return self.factors["tol"] > 0

    def solve(self, problem):
        """
        Run a single macroreplication of a solver on a problem.

        Arguments
        ---------
        problem : Problem object
            simulation-optimization problem to solve
        crn_across_solns : bool
            indicates if CRN are used when simulating different solutions

        Returns
        -------
        recommended_solns : list of Solution objects
            list of solutions recommended throughout the budget
        intermediate_budgets : list of ints
            list of intermediate budgets when recommended solutions changes
        """
        recommended_solns = []
        intermediate_budgets = []
        expended_budget = 0

        # Default values.
        r = self.factors["r"]
        tol = self.factors["tol"]
        theta = self.factors["theta"]
        gamma = self.factors["gamma"]
        alpha_max = self.factors["alpha_max"]
        alpha_0 = self.factors["alpha_0"]
        c = self.factors["c"]
        q = self.factors["q"]
        set_size = self.factors["set_size"]

        # Upper bound and lower bound.
        lower_bound = np.array(problem.lower_bounds)
        upper_bound = np.array(problem.upper_bounds)
    
        # Initialize stepsize.
        alpha = alpha_0

        # Input inequality and equlaity constraint matrix and vector.
        # Cix <= di
        # Cex = de
        Ci = problem.Ci
        di = problem.di
        Ce = problem.Ce
        de = problem.de

        # Checker for whether the problem is unconstrained.
        unconstr_flag = (Ce is None) & (Ci is None) & (di is None) & (de is None) & (all(np.isinf(lower_bound))) & (all(np.isinf(upper_bound)))

        # Start with the initial solution.
        new_solution = self.create_new_solution(problem.factors["initial_solution"], problem)
        new_x = new_solution.x

        # If the initial solution is not feasible, generate one using phase one simplex.
        if (not unconstr_flag) & (not self._feasible(new_x, problem, tol)):
            new_x = self.find_feasible_initial(problem, Ce, Ci, de, di, tol)
            new_solution = self.create_new_solution(tuple(new_x), problem)
        
        # Use r simulated observations to estimate the objective value.
        problem.simulate(new_solution, r)
        expended_budget += r
        best_solution = new_solution
        recommended_solns.append(new_solution)
        intermediate_budgets.append(expended_budget)

        while expended_budget < problem.factors["budget"]:
            new_x = new_solution.x

            # Poll Step.
            # Choose a set of non-zero polling directions.
            dirs = set()
            for _ in range(set_size):
                weight = [self.rng_list[0].uniform(0, 1) for _ in range(problem.dim)]
                dir = self.search_dir(problem, new_x, Ce, Ci, de, di, weight)
                print('dir', dir)
                if not (np.allclose(dir, np.zeros(problem.dim), rtol=0, atol=tol)):
                    dirs.add(tuple(dir))

            flag = False # Flag for whether a feasible sufficient decrease polling direction is found.       
            while len(dirs) > 0:
                # Randomly choose a polling direction.
                dir = self.rng_list[1].choices(list(dirs))[0]
                dirs.remove(dir)
                # Get a temp solution.
                dir = np.array(dir)
                candidate_x = new_x + alpha * dir
                candidate_solution = self.create_new_solution(tuple(candidate_x), problem)
                # Use r simulated observations to estimate the objective value.
                problem.simulate(candidate_solution, r)
                expended_budget += r

                # Check sufficient decrease condition
                if (-1 * problem.minmax[0] * candidate_solution.objectives_mean) <= (
                                    -1 * problem.minmax[0] * new_solution.objectives_mean - c * alpha**q):
                    # Successful step.
                    flag = True
                    # Update solution.
                    new_solution = candidate_solution
                    # Increase step size.
                    alpha = min(alpha_max, alpha * gamma)
                    break

            # Unsucessful step.
            if not flag:
                # Decrease step size.
                alpha *= theta

            # Append new solution.
            if (problem.minmax[0] * new_solution.objectives_mean > problem.minmax[0] * best_solution.objectives_mean):
                best_solution = new_solution
                recommended_solns.append(new_solution)
                intermediate_budgets.append(expended_budget)

        print('solutions', [sol.x for sol in recommended_solns])
        return recommended_solns, intermediate_budgets

    def _feasible(self, x, problem, tol):
        """
        Check whether a solution x is feasible to the problem.
        
        Arguments
        ---------
        x : tuple
            a solution vector
        problem : Problem object
            simulation-optimization problem to solve
        tol: float
            Floating point comparison tolerance
        """
        res = True
        if (problem.Ci is not None) and (problem.di is not None):
            res = res & np.all(problem.Ci @ x <= problem.di + tol)
        if (problem.Ce is not None) and (problem.de is not None):
            res = res & (np.allclose(np.dot(problem.Ce, x), problem.de, rtol=0, atol=tol))
        return res & (np.all(x >= problem.lower_bounds)) & (np.all(x <= problem.upper_bounds))
    
    def search_dir(self, problem, x, Ae, Ai, be, bi, weight):
        """
        Project the vector x onto the hyperplane H: Ae x = be, Ai x <= bi by solving a quadratic projection problem:

        min d^Td
        s.t. Ae(x + d) = be
             Ai(x + d) <= bi
             (x + d) >= lb
             (x + d) <= ub
        
        Arguments
        ---------
        problem : Problem object
            simulation-optimization problem to solve
        x : ndarray
            vector to be projected
        Ae: ndarray
            equality constraint coefficient matrix
        be: ndarray
            equality constraint coefficient vector
        Ai: ndarray
            inequality constraint coefficient matrix
        bi: ndarray
            inequality constraint coefficient vector 
        Returns
        -------
        x_new : ndarray
            the projected vector
        """
        # Define variables.
        d = cp.Variable(problem.dim)

        # Define objective.
        obj = cp.Minimize(cp.quad_form(d, np.identity(problem.dim)))

        # Define constraints.
        constraints = []
        if (Ae is not None) and (be is not None):
            constraints.append(Ae @ (x + d) == be.ravel())
        if (Ai is not None) and (bi is not None):
            constraints.append(Ai @ (x + d) <= bi.ravel())

        upper_bound = np.array(problem.upper_bounds)
        lower_bound = np.array(problem.lower_bounds)

        # Removing redundant bound constraints.
        ub_inf_idx = np.where(~np.isinf(upper_bound))[0]
        if len(ub_inf_idx) > 0:
            for i in ub_inf_idx:
                constraints.append((x + d)[i] <= upper_bound[i])
        lb_inf_idx = np.where(~np.isinf(lower_bound))[0]
        if len(lb_inf_idx) > 0:
            for i in lb_inf_idx:
                constraints.append((x + d)[i] >= lower_bound[i])
        # Form and solve problem.
        prob = cp.Problem(obj, constraints)
        prob.solve()

        dir = d.value


        # # Avoid floating point error
        # dir[np.abs(dir) < self.factors["tol"]] = 0

        return dir


    def find_feasible_initial(self, problem, Ae, Ai, be, bi, tol):
        '''
        Find an initial feasible solution (if not user-provided)
        by solving phase one simplex.

        Arguments
        ---------
        problem : Problem object
            simulation-optimization problem to solve
        C: ndarray
            constraint coefficient matrix
        d: ndarray
            constraint coefficient vector

        Returns
        -------
        x0 : ndarray
            an initial feasible solution
        tol: float
            Floating point comparison tolerance
        '''
        upper_bound = np.array(problem.upper_bounds)
        lower_bound = np.array(problem.lower_bounds)

        # Define decision variables.
        x = cp.Variable(problem.dim)

        # Define constraints.
        constraints = []

        if (Ae is not None) and (be is not None):
            constraints.append(Ae @ x == be.ravel())
        if (Ai is not None) and (bi is not None):
            constraints.append(Ai @ x <= bi.ravel())

        # Removing redundant bound constraints.
        ub_inf_idx = np.where(~np.isinf(upper_bound))[0]
        if len(ub_inf_idx) > 0:
            for i in ub_inf_idx:
                constraints.append(x[i] <= upper_bound[i])
        lb_inf_idx = np.where(~np.isinf(lower_bound))[0]
        if len(lb_inf_idx) > 0:
            for i in lb_inf_idx:
                constraints.append(x[i] >= lower_bound[i])

        # Define objective function.
        obj = cp.Minimize(0)
        
        # Create problem.
        model = cp.Problem(obj, constraints)

        # Solve problem.
        model.solve(solver = cp.SCIPY)

        # Check for optimality.
        if model.status not in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE] :
            raise ValueError("Could not find feasible x0")
        x0 = x.value
        if not self._feasible(x0, problem, tol):
            raise ValueError("Could not find feasible x0")

        return x0
