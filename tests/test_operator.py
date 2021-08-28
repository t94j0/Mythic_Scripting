import pytest

from mythic import mythic_rest
from tests.util.fixtures import mythic, random_string, USERNAME


@pytest.mark.asyncio
async def test_integration_get_self(mythic: mythic_rest.Mythic):
    operator = await mythic.get_self()
    operator_obj = operator.response
    assert operator_obj.username == USERNAME


@pytest.mark.skip(reason='Return mythic_rest.Operator')
@pytest.mark.asyncio
async def test_integration_get_self_desired(mythic: mythic_rest.Mythic):
    operator = await mythic.get_self()
    operator_obj = operator
    assert operator_obj.username == USERNAME


@pytest.mark.asyncio
async def test_integration_create_operator(mythic: mythic_rest.Mythic, random_string: str):
    op = mythic_rest.Operator(
        username=random_string, password='testtesttest', admin=False)
    created_operator = await mythic.create_operator(op)
    operator = await mythic.get_operator(created_operator.response)
    assert operator.response.username == random_string


@pytest.mark.skip(reason='create_operator takes a username and password since those are the only fields used by the create_operator function')
@pytest.mark.asyncio
async def test_integration_create_operator_desired(mythic: mythic_rest.Mythic):
    created_operator = await mythic.create_operator('TEST', 'password')
    operator = await mythic.get_operator(created_operator.username)
    assert operator.username == 'TEST'


@pytest.mark.asyncio
async def test_integration_get_operator(mythic: mythic_rest.Mythic):
    op = mythic_rest.Operator(username=USERNAME)
    populated_op = await mythic.get_operator(op)
    assert populated_op.response.username == USERNAME


@pytest.mark.skip(reason='Make a get_operator take a string with a username instead of having to construct an Operator object')
@pytest.mark.asyncio
async def test_integration_get_operator_desired(mythic: mythic_rest.Mythic):
    operator = await mythic.get_operator(USERNAME)
    assert operator.username == USERNAME


@pytest.mark.skip(reason='Make a get_operator_by_id take a string with an id instead of having to construct an Operator object')
@pytest.mark.asyncio
async def test_integration_get_operator_by_id_desired(mythic: mythic_rest.Mythic):
    my_operator = await mythic.get_self()
    populated_op = await mythic.get_operator_by_id(my_operator.id)
    assert populated_op.username == USERNAME


@pytest.mark.skip(reason='Create a delete_operator function to remove an operator from Mythic entirely')
@pytest.mark.asyncio
async def test_integration_delete_operator(mythic: mythic_rest.Mythic):
    # Setup
    created_operator = await mythic.create_operator('TEST', 'password')

    # Body
    populated_op = await mythic.delete_operator('TEST')
    assert (await mythic.get_operator('TEST')) is None
