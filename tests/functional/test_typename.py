import pytest

from tartiflette import Resolver
from tartiflette.executors.types import Info
from tartiflette.engine import Engine


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
        query aquery {
            test(choose:1){
                ... on One {
                    __typename
                    aField
                    bField
                }
                ... on Two {
                    __typename
                    cField
                    dField
                }
                ... on Three {
                    __typename
                    eField
                    fField
                }
            }
            __typename
        }
        """,
            {
                "data": {
                    "test": {
                        "__typename": "One",
                        "aField": "aValue",
                        "bField": 1,
                    },
                    "__typename": "Query",
                }
            },
        ),
        (
            """
        query aquery {
            test(choose:2){
                ... on One {
                    __typename
                    aField
                    bField
                }
                ... on Two {
                    __typename
                    cField
                    dField
                }
                ... on Three {
                    __typename
                    eField
                    fField
                }
            }
            __typename
        }
        """,
            {
                "data": {
                    "test": {
                        "__typename": "Two",
                        "cField": 2,
                        "dField": "dValue",
                    },
                    "__typename": "Query",
                }
            },
        ),
        (
            """
        query aquery {
            test(choose:3){

                ... on One {
                    __typename
                    aField
                    bField
                }
                ... on Two {
                    __typename
                    cField
                    dField
                }
                ... on Three {
                    __typename
                    eField
                    fField
                }
            }
            __typename
        }
        """,
            {
                "data": {
                    "test": {
                        "__typename": "Three",
                        "eField": 3.6,
                        "fField": "fValue",
                    },
                    "__typename": "Query",
                }
            },
        ),
    ],
)
async def test_tartiflette_typename(query, expected, clean_registry):
    schema_sdl = """
    type One {
        aField: String
        bField: Int
    }

    type Two {
        cField: Int
        dField: String
    }

    type Three {
        eField: Float
        fField: String
    }

    union Mixed = One | Two | Three

    type Query {
        test(choose: Int!): Mixed
    }
    """

    @Resolver("Query.test")
    async def func_field_resolver(parent, arguments, request_ctx, info: Info):
        chosen = arguments.get("choose", 0)
        if chosen == 1:
            return {"aField": "aValue", "bField": 1, "_typename": "One"}
        elif chosen == 2:

            class Lol:
                def __init__(self, *args, **kwargs):
                    self._typename = "Two"
                    self.cField = 2
                    self.dField = "dValue"

            return Lol()
        elif chosen == 3:

            class Three:
                def __init__(self, *args, **kwargs):
                    self.eField = 3.6
                    self.fField = "fValue"

            return Three()

        return None

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(query)

    assert expected == result