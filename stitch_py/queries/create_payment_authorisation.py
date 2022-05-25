from enum import Enum
from typing import TypedDict

from gql import gql

from .shared_types import BankId


class Payer(TypedDict):
    email: str
    name: str
    reference: str
    phoneNumber: str


class BeneficiaryType(str, Enum):
    Public = 'public'
    Private = 'private'


class AccountType(str, Enum):
    Current = 'current'
    Savings = 'savings'
    Credit = 'credit'
    Loan = 'loan'
    Investment = 'investment'
    Other = 'other'
    Unknown = 'unknown'


class LinkPayBankAccount(TypedDict):
    name: str
    bankId: BankId
    accountNumber: str
    accountType: AccountType
    beneficiaryType: BeneficiaryType
    reference: str


class InitialPayment(TypedDict):
    amount: str
    external_reference: str


query = gql(
    """
    mutation CreatePaymentAuthorisation(
      $beneficiary: ClientPaymentAuthorizationRequestCreateBeneficiaryInput!,
      $payer: ClientPaymentAuthorizationRequestCreatePayerInput!,
      $initialPayment: ClientPaymentAuthorizationRequestCreateInitialPaymentInput,
    ) {
      clientPaymentAuthorizationRequestCreate(
        input: {
          beneficiary: $beneficiary,
          payer: $payer,
          initialPayment: $initialPayment,
        }
      ) {
        authorizationRequestUrl
      }
    }
    """,
)
