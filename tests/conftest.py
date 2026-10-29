"""Small legal framed cities for deterministic rule tests."""

import pytest
from taxishare.config import Config
from taxishare.city import Building
from taxishare.scenario import Scenario, TaxiInitial, Request


@pytest.fixture
def ring_scenario():
    def build(requests=((0, 0, 2, 0),), fleet=((0, (0, 0), (0, -1)),), **options):
        config = Config(**{**dict(width=7, height=7, horizontal_axes=2, vertical_axes=2,
                                 buildings=4, taxis=len(fleet), requests=len(requests),
                                 appearance_seconds=10, max_seconds=1000), **options})
        buildings = (Building(0, (1, 1), (1, 0)), Building(1, (3, 1), (3, 0)),
                     Building(2, (5, 1), (5, 0)), Building(3, (5, 5), (5, 6)))
        return Scenario(config, (0, 6), (0, 6), buildings,
                        tuple(TaxiInitial(*t) for t in fleet), tuple(Request(*r) for r in requests))
    return build
