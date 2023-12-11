import pytest
import allure
from src.delivery import DeliveryPrice
from src.model import Cargo, Size, WorkloadRate, CalculatePriceException
from logging import getLogger

logger = getLogger(__name__)


class TestDelivery:

    @allure.title("Get fee based on distance")
    @pytest.mark.parametrize(
        "distance, expected", (
                (1, 50),
                (9, 100),
                (10, 200),
                (30, 300),
                (100, 300)
        ))
    def test_distance(self, distance, expected) -> None:
        """
        checking dependencies distance from price (unit test)
        """
        assert DeliveryPrice.get_fee_for_distance(distance) == expected, "Price is wrong"

    @allure.title("Invalid distance value")
    @pytest.mark.parametrize("distance", (0, -1, "hello yandex"))
    def test_wrong_value_distance(self, distance) -> None:
        cargo = Cargo(Size.SMALL, True)
        with pytest.raises(ValueError):
            DeliveryPrice(WorkloadRate.OTHER, cargo, -1)

    @allure.title("Get fee based on size")
    @pytest.mark.parametrize("size, expected", ((Size.SMALL, 100), (Size.BIG, 200)))
    def test_size(self, size, expected):
        """
        checking dependencies size from price (unit test)
        """
        cargo = Cargo(size, False)
        assert DeliveryPrice.get_fee_for_size(cargo) == expected, "Price is wrong"

    @allure.title("Get fee based on fragility")
    @pytest.mark.parametrize("fragility, expected", ((True, 300),  (False, 0)))
    def test_fragility(self, fragility, expected):
        """
        checking dependencies fragility from price (unit test)
        """
        cargo = Cargo(Size.BIG, fragility)
        assert DeliveryPrice.get_fee_for_fragility(cargo) == expected, "Price is wrong"

    @allure.title("Get minimal price for very low final price")
    def test_minimal_price(self):
        """
        Small size (100) + not fragility (0) * Workload rate 1.0 + distance (50) = 150
        But final price is 400
        """
        cargo = Cargo(Size.SMALL, False)
        delivery = DeliveryPrice(WorkloadRate.OTHER, cargo, 1)
        assert delivery.calculate_price() == 400

    @allure.title("Now allowed move fragility more then 30km")
    def test_fragility_to_long_distance(self):
        """
        raise CalculatePriceException because fragility and more than 30km
        """
        cargo = Cargo(Size.SMALL, True)
        with pytest.raises(CalculatePriceException):
            DeliveryPrice(WorkloadRate.OTHER, cargo, 31).calculate_price()

    @allure.title("Check workload rate")
    @pytest.mark.parametrize("rate", (WorkloadRate.VERY_HIGH, WorkloadRate.HIGH, WorkloadRate.OTHER))
    def test_workload_rate(self, rate):
        """
        Check workload rate param
        """
        cargo = Cargo(Size.BIG, True)
        price = DeliveryPrice(rate, cargo, 20).calculate_price()
        assert (300+200+200)*rate.value == price
