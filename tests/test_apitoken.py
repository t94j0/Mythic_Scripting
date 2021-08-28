import pytest

from mythic import mythic_rest
from tests.util.fixtures import mythic, USERNAME, PASSWORD, SERVER_IP, SERVER_PORT


async def remove_all_apitokens(client: mythic_rest.Mythic):
    resp = await client.get_apitokens()
    for token in resp.response:
        await client.remove_apitoken(token)


@pytest.mark.asyncio
async def test_integration_apitoken(mythic: mythic_rest.Mythic):
    await remove_all_apitokens(mythic)
    await mythic.create_apitoken()
    tokens = (await mythic.get_apitokens()).response
    assert len(tokens) == 1


@pytest.mark.skip(reason='Goal')
@pytest.mark.asyncio
async def test_no_login():
    client = mythic_rest.Mythic(
        username=USERNAME, password=PASSWORD, server_ip=SERVER_IP, server_port=SERVER_PORT, ssl=True)
    with pytest.raises(mythic_rest.MythicUnauthenticatedError):
        await client.get_apitokens()
