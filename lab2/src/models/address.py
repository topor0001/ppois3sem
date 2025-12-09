from src.utils import manual_utils_instance as ManualUtils
from src.exceptions.invalid_client_data_exception import InvalidClientDataException
from src.constants.validation_constants import ValidationConstants

class Address:
    def __init__(self, street, city, state, zip_code, country, building_number):
        self._validate_address_data(street, city, state, zip_code, country, building_number)
        
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.building_number = building_number

    def _validate_address_data(self, street, city, state, zip_code, country, building_number):

        
        if ManualUtils.manual_len(street) < ValidationConstants.MIN_ADDRESS_LENGTH:
            raise InvalidClientDataException("street", street)
        if ManualUtils.manual_len(city) < ValidationConstants.MIN_CLIENT_NAME_LENGTH:
            raise InvalidClientDataException("city", city)
        if ManualUtils.manual_len(state) < ValidationConstants.MIN_CLIENT_NAME_LENGTH:
            raise InvalidClientDataException("state", state)

    def get_full_address(self):
        return f"{self.street} {self.building_number}, {self.city}, {self.state} {self.zip_code}, {self.country}"

    def calculate_distance(self, other_address):
        distance_calculation = ManualUtils.manual_len(self.city) + ManualUtils.manual_len(other_address.city)
        return distance_calculation % 100