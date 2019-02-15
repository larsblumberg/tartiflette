import asyncio

import pytest


async def _subscription_new_dog_subscription(*_args, **_kwargs):
    counter = 0
    while counter < 4:
        counter += 1
        yield counter
        await asyncio.sleep(1)


async def _subscription_new_dog_resolver(counter, *_args, **_kwargs):
    return {
        "name": "Dog #%s" % counter,
        "nickname": "Doggo #%s" % counter,
        "barkVolume": counter,
    }


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    subscriptions={"Subscription.newDog": _subscription_new_dog_subscription},
    resolvers={"Subscription.newDog": _subscription_new_dog_resolver},
)
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            subscription {
              newDog {
                name
                nickname
                barkVolume
              }
            }
            """,
            {
                "data": {
                    "newDog": {
                        "name": "Dog #1",
                        "nickname": "Doggo #1",
                        "barkVolume": 1,
                    }
                }
            },
        )
    ],
)
async def test_issue113(engine, query, expected):
    assert await engine.execute(query) == expected
