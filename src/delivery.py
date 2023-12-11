from src.model import WorkloadRate, Cargo, Size, CalculatePriceException

from logging import getLogger

logger = getLogger(__name__)


class DeliveryPrice:

    MIN_PRICE = 400

    def __init__(self, workload_rate: WorkloadRate, cargo: Cargo, distance: float) -> None:
        self.workload_rate = workload_rate
        self.cargo = cargo
        self.distance = self.__validate_distance(distance)
        logger.info(f"Cargo is {self.cargo.__repr__()}. Workload rate is {workload_rate.value}. Distance is {distance}")

    @staticmethod
    def __validate_distance(distance: float | int) -> float | int:
        if not isinstance(distance, (int, float)) or distance <= 0:
            raise ValueError("Input must be a number greater than 0.")
        else:
            return distance

    @staticmethod
    def get_fee_for_distance(distance: float) -> int:
        """
        kilometers
        :return:
        """
        if distance < 2:
            distance_price = 50
        elif distance < 10:
            distance_price = 100
        elif distance < 30:
            distance_price = 200
        else:
            distance_price = 300
        return distance_price

    @staticmethod
    def get_fee_for_size(cargo: Cargo) -> int:
        return 200 if cargo.size == Size.BIG else 100

    @staticmethod
    def get_fee_for_fragility(cargo: Cargo) -> int:
        return 300 if cargo.fragility else 0

    def calculate_price(self):

        if self.cargo.fragility and self.distance > 30:
            raise CalculatePriceException("Can't deliver fragility cargo for distance more then 30km")

        price = self.get_fee_for_distance(self.distance)
        price += self.get_fee_for_size(self.cargo)
        price += self.get_fee_for_fragility(self.cargo)
        price *= self.workload_rate.value

        logger.info(f"Final price is {price}")
        return price if price > self.MIN_PRICE else self.MIN_PRICE

