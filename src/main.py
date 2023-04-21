from fastapi import FastAPI
import logging
import typing
from lib.classes import PayloadBody, Contract, SuccessfulResponse, Manager

# Creating a new webserver instance
app = FastAPI()


@app.get("/testing")
async def testing():
    return {"message": "Test is successful!"}


@app.post("/spaceship/optimize", response_model=SuccessfulResponse)
async def process_payload(request_payload: PayloadBody):

    # Creating a list of contracts
    contracts_list: typing.List[Contract] = list()

    # All validation of the PayloadBody and the PayloadContract should be done by validation methods in the Pydantic classes
    for i, payload_contract in enumerate(request_payload.contracts_list):
        # Creating a new contract
        contract = Contract(
            contract_number=i,
            contract_name=payload_contract.name,
            start_hour=payload_contract.start,
            duration=payload_contract.duration,
            price=payload_contract.price,
        )

        # Adding the newly created contract into the list of contracts
        contracts_list.append(contract)

    # pdbst()

    # Creating the manager
    manager = Manager(contracts=contracts_list)

    # Running the manager
    optimal_state = manager.run()

    # Getting the parameters from the optimal state
    optimal_contracts: typing.List[Contract] = [i for i in optimal_state.contracts]
    optimal_contracts.sort(key=lambda x: x.duration_range[0])

    income: int = sum(
        i.penalty for i in optimal_contracts
    )  # Note: The penalty is equivalent to the price - Essentially if the job is not taken, the price becomes the penalty.
    path: typing.List[str] = [i.contract_name for i in optimal_contracts]

    # Constructing the response
    response: SuccessfulResponse = SuccessfulResponse(income=income, path=path)

    return response
