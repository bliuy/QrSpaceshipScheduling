from __future__ import annotations
import typing
import bisect
import copy
import collections

DurationRange: typing.TypeAlias = typing.Tuple[
    int, int
]  # Represents the start and end dates inclusive of a rental duration.


def is_overlaps(range_one: DurationRange, range_two: DurationRange) -> bool:
    """
    If the ranges overlaps, this function will return True. Returns False otherwise.
    """

    # Defining the ranges
    s1 = range_one[0]
    e1 = range_one[1]
    s2 = range_two[0]
    e2 = range_two[1]

    return max(s1, s2) < min(e1, e2)


class Contract:


    # def __init__(self, contract_number: int, duration_range: DurationRange, penalty: int) -> None:
    #     self.contract_number: int = contract_number
    #     self.duration_range: DurationRange = duration_range
    #     self.penalty: int = penalty

    def __init__(self, contract_number: int, contract_name: str, start_hour: int, duration: int, price: int) -> None:


        self.contract_number: int = contract_number
        self.contract_name: str = contract_name

        # Calculating the duration range
        duration_range: DurationRange = (start_hour, start_hour + duration)
        self.duration_range: DurationRange = duration_range

        self.penalty: int = price # Price == Penalty since we miss out on this reward if this contract is not done.

        return None
    
class State:
    def __init__(self) -> None:
        self.contracts: typing.List[
            Contract
        ] = []  # Keeping track of the number of contracts present in the current state
        self.occupied_durations: typing.List[
            DurationRange
        ] = []  # Storing the various durations of the rentals
        self.upper: int = int((2**128) - 1)  # Equivalent to upper limit of unsigned 128 bit integer. Assuming that system does not deal with values bigger than this.
        self.cost: int = 0  # No costs at the initial stage
        return None

    def no_overlapping_duration(self, duration_to_check: DurationRange) -> bool:
        if len(self.occupied_durations) == 0:
            return (
                True  # will never overlap since there are no durations in the list yet.
            )
        else:
            insertion_pos: int = bisect.bisect(
                a=self.occupied_durations,
                x=duration_to_check[0],
                key=lambda x: x[0],  # sorted by the starting time
            )

            # Checking if overlapping prior range
            if insertion_pos > 0:
                prior_duration_range: DurationRange = self.occupied_durations[
                    insertion_pos - 1
                ]
                if is_overlaps(prior_duration_range, duration_to_check):
                    return False

            # Checking if overlapping subsequent range
            if insertion_pos < len(self.occupied_durations):
                subsequent_duration_range: DurationRange = self.occupied_durations[
                    insertion_pos
                ]
                if is_overlaps(duration_to_check, subsequent_duration_range):
                    return False

            return True

    def get_max_contract_number(self) -> typing.Optional[int]:

        if len(self.contracts) == 0:
            return None
        else:
            return max(i.contract_number for i in self.contracts)

    def get_all_contract_numbers(self) -> typing.Set[int]:
        return set(i.contract_number for i in self.contracts)


    def add_contract(self, contract: Contract, upper: int, cost: int) -> typing.Optional[State]:
        
        # Check if there is any overlaps in terms of durations
        if not self.no_overlapping_duration(contract.duration_range):
            return None
        
        # Making a copy of the current state
        new_state: State = copy.deepcopy(self)

        # Append the valid contract to the state
        new_state.contracts.append(contract)
        bisect.insort(new_state.occupied_durations, contract.duration_range, key=lambda x: x[0]) # Adding the time occupied by this new contract as well

        # Updating the upper_bound and cost values of the new state
        new_state.upper = upper
        new_state.cost = cost

        # Returning the new state
        return new_state

class Manager:
    
    def __init__(self, contracts: typing.Iterable[Contract]) -> None:

        # Capturing the list of contracts
        contracts_list: typing.List[Contract] = list(contracts) # Converting the iterable into a list
        contracts_list.sort(key=lambda x: x.contract_number) # Sorting the list by ascending contract numbers
        self.contracts_list: typing.List[Contract] = contracts_list # Storing the list of contracts in this current manager instance

        # # Creating a list to store all states
        # self.unprocessed_states: collections.deque[State] = collections.deque()
        # self.processed_states: typing.List[State] = list()
        
        # # Creating an initial state
        # initial_state: State = State() # Empty state

        # # Creating & updating the global upper bound
        # self.global_upper: int = initial_state.upper # Should be ~ inf

        # # Adding the initial state into the states list
        # self.unprocessed_states.append(
        #     copy.deepcopy(
        #         initial_state
        #     )
        # )

        return None

    def run(self) -> State:

        # Setup
        unprocessed_states: collections.deque[State] = collections.deque()
        # processed_states: typing.List[State] = list()
        contract_indexes: typing.List[int] = list(i for i in range(len(self.contracts_list)))

        # Creating an initial state
        initial_state: State = State() # Empty state

        ## Using the initial state value as the global upper bound
        global_upper: int = initial_state.upper

        ## Adding the initial state to the queue of unprocessed states
        unprocessed_states.append(
            initial_state
        )

        ## Setting the initial state as the optimal state
        optimal_state: State = initial_state

        # Building the branch and bound tree
        while len(unprocessed_states) > 0:

            current_state: State = unprocessed_states.popleft() # FIFO

            # Checking if current state is optimal
            if current_state.cost > global_upper:
                continue # Indicates that the lower bound is already not optimal
            else:
                if current_state.upper < global_upper: # Indicates that this state is better than the previous ones
                    global_upper = current_state.upper
                    optimal_state = current_state
            
            # Spawning sub nodes
            # Determining the possible contracts that we are allowed to create based on this state
            current_contract_number = current_state.get_max_contract_number()
            if current_contract_number is None:
                possible_idx = contract_indexes
            else:
                possible_idx = [i for i in contract_indexes if i > current_contract_number]
            
            ## Checking if any possible nodes left to spawn
            if len(possible_idx) == 0:
                continue
            else:
                for idx in possible_idx:

                    # Getting the contract
                    selected_contract = self.contracts_list[idx]

                    # Calculating the upper bound
                    ub_idx = set(contract_indexes) # Set of all possible indexes
                    ub_idx.remove(idx) # Removing the current index
                    ub_idx = ub_idx - current_state.get_all_contract_numbers() # Excluding all visited indexes
                    current_upper: int = sum(c.penalty for c in map(self.contracts_list.__getitem__, ub_idx))

                    # Calculating the cost value
                    c_idx = set(contract_indexes)
                    c_idx.remove(idx)
                    c_idx = c_idx - current_state.get_all_contract_numbers()
                    c_idx = set(i for i in c_idx if i < idx)
                    current_cost: int = sum(c.penalty for c in map(self.contracts_list.__getitem__, c_idx))

                    # Attempting to create a new state based on the current parameters
                    new_state = current_state.add_contract(
                        contract=selected_contract,
                        upper=current_upper,
                        cost=current_cost
                    )

                    if new_state is not None:
                        unprocessed_states.append(new_state)
            
        return optimal_state


# Testing function
contracts = [
    Contract(0, "foo0", 0, 5, 10),
    Contract(1, "foo1", 3, 7, 14),
    Contract(2, "foo2", 5, 9, 8),
    Contract(3, "foo3", 5, 9, 7),
]

manager = Manager(contracts=contracts)
optimal = manager.run()
print([c.contract_name for c in  optimal.contracts])








        









    

