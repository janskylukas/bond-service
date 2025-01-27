from rest_framework.serializers import ValidationError


class InvalidISINError(ValidationError):
    def __init__(self, isin: str):
        super().__init__(f"Invalid ISIN: {isin}")
