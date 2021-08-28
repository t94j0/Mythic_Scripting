from random import random
import pytest

from mythic import mythic_rest
from tests.util.fixtures import mythic, random_string, USERNAME


@pytest.mark.asyncio
async def test_integration_get_all_operations(mythic: mythic_rest.Mythic):
    ops = await mythic.get_all_operations()
    assert len(ops.response) > 0


@pytest.mark.asyncio
async def test_integration_create_operation(mythic: mythic_rest.Mythic, random_string: str):
    operator = (await mythic.get_self()).response
    new_operation = mythic_rest.Operation(name=random_string, admin=operator)
    op = await mythic.create_operation(new_operation)
    assert op.response.name == random_string
    assert op.response.admin.username == USERNAME


@pytest.mark.skip(reason='Create operation should raise an error if operation does not have admin')
@pytest.mark.asyncio
async def test_integration_create_operation_desired(mythic: mythic_rest.Mythic):
    NAME = 'NEWOP'
    new_operation = mythic_rest.Operation(name=NAME)
    op = await mythic.create_operation(new_operation)
    assert op.name == NAME


@pytest.mark.skip(reason='create_operation should take a name and admin instead of an object. Not easy to know which fields need to be populated in large object')
@pytest.mark.asyncio
async def test_integration_create_operation_desired(mythic: mythic_rest.Mythic, random_string: str):
    my_user = await mythic.get_self()
    op = await mythic.create_operation(random_string, my_user.username)
    assert op.name == random_string


@pytest.mark.asyncio
async def test_integration_get_operation(mythic: mythic_rest.Mythic, random_string: str):
    operator = (await mythic.get_self()).response
    new_operation = mythic_rest.Operation(name=random_string, admin=operator)
    op_create = await mythic.create_operation(new_operation)
    operation = await mythic.get_operation(op_create.response)
    assert operation.response.name == random_string


@pytest.mark.skip(reason='It would be really nice to have an operation ID or some other identification that could be searched')
@pytest.mark.asyncio
async def test_integration_get_operation_desired(mythic: mythic_rest.Mythic, random_string: str):
    my_user = await mythic.get_self()
    op_create = await mythic.create_operation(random_string, my_user.username)
    operation = await mythic.get_operation_by_id(op_create.id)
    assert operation.response.name == random_string


@pytest.mark.asyncio
async def test_integration_add_to_operation(mythic: mythic_rest.Mythic, random_string: str):
    operator_name = f'{random_string}OPERATOR'
    operation_name = f'{random_string}OPERATION'

    op = mythic_rest.Operator(
        username=operator_name, password='testtesttest', admin=False)
    created_operator = await mythic.create_operator(op)
    operator = await mythic.get_operator(created_operator.response)

    my_operator = (await mythic.get_self()).response
    new_operation = mythic_rest.Operation(
        name=operation_name, admin=my_operator)
    operation = await mythic.create_operation(new_operation)

    updated_operation = await mythic.add_or_update_operator_for_operation(operation.response, operator.response)
    assert updated_operation.response.admin.username == my_operator.username
    assert updated_operation.response.members[0].username == operator.response.username
