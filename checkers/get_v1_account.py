from datetime import datetime

from hamcrest import (
    assert_that,
    starts_with,
    has_property,
    instance_of,
    has_properties,
    equal_to,
    all_of,
)


class GetV1Account:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    @classmethod
    def check_response_values(
            cls,
            response
    ):
        registr_date = "2024-10-24"
        assert_that(str(response.resource.registration.date()), equal_to(registr_date))
        assert_that(
            response, all_of(
                has_property("resource", has_property("login", starts_with("paveltest"))),
                has_property("resource", has_property("registration", instance_of(datetime))),
                has_property(
                    "resource", has_properties(
                        {
                            "rating": has_properties(
                                {
                                    "enabled": equal_to(True),
                                    "quality": equal_to(0),
                                    "quantity": equal_to(0)
                                }
                            )
                        }
                    )
                )
            )
        )