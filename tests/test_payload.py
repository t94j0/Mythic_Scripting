import pytest

from mythic import mythic_rest

from tests.util.fixtures import mythic

@pytest.mark.asyncio
async def test_payload_generate_mod_rewrite(mythic: mythic_rest.Mythic):
    '''
    precondition: a single payload must be generated
    '''
    ps = await mythic.get_payloads()
    target_uuid = ps.response[0].uuid
    res = await mythic.generate_mod_rewrite(target_uuid)
    # Need to think of a better test case
    assert '############' in res