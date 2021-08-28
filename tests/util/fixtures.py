
import pytest
from mythic import mythic_rest
import random
import string
from yaml import load, Loader

with open('./config.yml') as f:
    data = load(f.read(), Loader=Loader)
    USERNAME = data['username']
    PASSWORD = data['password']
    SERVER_IP = data['server_ip']
    SERVER_PORT = data['server_port']


@pytest.fixture
async def mythic() -> mythic_rest.Mythic:
    client = mythic_rest.Mythic(
        username=USERNAME, password=PASSWORD, server_ip=SERVER_IP, server_port=SERVER_PORT, ssl=True)
    await client.login()
    return client


@pytest.fixture
def random_string() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
