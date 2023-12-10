import pytest

from src.delivery import DeliveryPrice
from src.model import Cargo, Size, WorkloadRate


class TestDelivery:

    def test_minimal_price(self):
        cargo = Cargo(Size.SMALL, False)
        delivery = DeliveryPrice(WorkloadRate.OTHER, cargo, 1)
        assert delivery.calculate_price() == 400

    def test_fragility_to_long_distance(self):
        cargo = Cargo(Size.SMALL, True)
        delivery = DeliveryPrice(WorkloadRate.OTHER, cargo, 31)

    @pytest.mark.parametrize("distance", (1, 5, 11, 30))
    def test_distance(self, distance):
        cargo = Cargo(Size.BIG, True)
        delivery = DeliveryPrice(WorkloadRate.OTHER, cargo, 31)

    @pytest.mark.parametrize("size", (Size.SMALL, Size.BIG))
    def test_size(self, size):
        cargo = Cargo(size, False)
        delivery = DeliveryPrice(WorkloadRate.OTHER, cargo, 31)

    @pytest.mark.parametrize("fragility", (True, False))
    def test_fragility(self, fragility):
        cargo = Cargo(Size.BIG, fragility)
        delivery = DeliveryPrice(WorkloadRate.OTHER, cargo, 1)

