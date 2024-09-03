from time import time
from typing import Any

import aiohttp

from bot.api.http import make_request
from bot.config import settings


async def get_version_config(
        http_client: aiohttp.ClientSession, config_version: str
) -> dict[Any, Any] | Any:
    response_json = await make_request(
        http_client,
        'GET',
        f'https://api.hamsterkombatgame.io/clicker/config/{config_version}',
        {},
        'getting Version Config',
    )

    return response_json


async def get_game_config(
        http_client: aiohttp.ClientSession,
) -> dict[Any, Any] | Any:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/config',
        {},
        'getting Game Config',
    )

    return response_json


async def add_by_ref(http_client: aiohttp.ClientSession) -> bool:
    check_ref_status = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/referrer-info',
        {},
        ignore_status=422,
        error_context="Checking referrer info"
    )

    # Проверяем наличие ключа 'referrer' или другого специфического ключа
    if 'referrer' not in check_ref_status or check_ref_status.get('referrer', {}).get('welcomeCoins') != 5000:
        add_referral = await make_request(
            http_client,
            'POST',
            'https://api.hamsterkombatgame.io/clicker/add-referral',
            {'authUserId': f'{settings.REF.split("kentId")[1]}'},
            ignore_status=422,
            error_context="Adding referral"
        )

        select_exchange = await make_request(
            http_client,
            'POST',
            'https://api.hamsterkombatgame.io/clicker/select-exchange',
            {
                'exchangeId': 'hamster',
            },
            ignore_status=422,
            error_context="Selecting exchange"
        )
        return True
    else:
        return False


async def get_profile_data(http_client: aiohttp.ClientSession) -> dict[str]:
    while True:
        response_json = await make_request(
            http_client,
            'POST',
            'https://api.hamsterkombatgame.io/clicker/sync',
            {},
            'getting Profile Data',
            ignore_status=422,
        )
        profile_data = response_json.get('clickerUser') or response_json.get('found', {}).get('clickerUser', {})
        return profile_data


async def get_ip_info(
        http_client: aiohttp.ClientSession
) -> dict:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/ip',
        {},
        'getting Ip Info',
    )
    return response_json


async def get_account_info(
        http_client: aiohttp.ClientSession
) -> dict:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/auth/account-info',
        {},
        'getting Account Info',
    )
    return response_json


async def get_skins(
        http_client: aiohttp.ClientSession
) -> dict:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/get-skin',
        {},
        'getting Skins',
    )
    return response_json


async def send_taps(
        http_client: aiohttp.ClientSession, available_energy: int, taps: int
) -> dict[Any, Any] | Any:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/tap',
        {
            'availableTaps': available_energy,
            'count': taps,
            'timestamp': int(time()),
        },
        'Tapping',
        ignore_status=422,
    )

    profile_data = response_json.get('clickerUser') or response_json.get('found', {}).get('clickerUser', {})

    return profile_data
