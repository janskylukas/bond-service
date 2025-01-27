import decimal

from dateutil import relativedelta
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models

logger = __import__("logging").getLogger(__name__)


class Bond(models.Model):
    """Bond model"""

    class FrequencyChoices(models.IntegerChoices):
        """The values of the frequencies is equal to number of months in frequency"""

        MONTHLY = 1, "monthly"
        ANNUALLY = 12, "annually"

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="owner",
        related_name="bonds",
    )
    name = models.CharField(max_length=255, help_text="Name of the bond issuance")
    isin = models.CharField(max_length=12, help_text="ISIN identifier")
    value = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        help_text="Bond value",
        validators=[
            validators.MinValueValidator(
                limit_value=decimal.Decimal(0),
                message="Value must be higher than 0",
            ),
        ],
    )
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Annual interest rate in percentage",
        validators=[
            validators.MinValueValidator(
                limit_value=decimal.Decimal(0),
                message="Interest rate must be higher than 0",
            ),
        ],
    )
    purchase_date = models.DateField(help_text="Date when the bond was purchased")
    maturity_date = models.DateField(help_text="Date when the bond matures")
    payment_frequency = models.PositiveSmallIntegerField(
        choices=FrequencyChoices.choices,
        default=FrequencyChoices.ANNUALLY,
        help_text="Frequency of interest payments",
    )

    class Meta:
        verbose_name = "Bond"
        verbose_name_plural = "Bonds"
        ordering = ["maturity_date"]

    def __str__(self):
        return self.name

    def clean(self):
        if self.maturity_date < self.purchase_date:
            msg = "Maturity date must be after purchase date"
            raise ValidationError(msg)

    @property
    def periods(self) -> int:
        delta = relativedelta.relativedelta(
            self.maturity_date,
            self.purchase_date,
        )

        months_delta = delta.years * 12 + delta.months

        return months_delta // self.payment_frequency

    @property
    def future_value(self) -> decimal.Decimal:
        with decimal.localcontext(prec=19):
            return round(
                decimal.Decimal(
                    value=self.value * (1 + self.interest_rate / 100) ** self.periods,
                ),
                2,
            )
