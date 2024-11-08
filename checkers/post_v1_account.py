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


class PostV1Account:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    @classmethod
    def check_response_values(
            cls,
            response
    ):
        today = str(datetime.utcnow().date())
        assert_that(str(response.resource.registration.date()), equal_to(today))
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