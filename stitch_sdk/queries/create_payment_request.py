from typing import TypedDict

from gql import gql

from .shared_types import BankId


class InstantPayBankAccount(TypedDict):
    name: str
    bankId: BankId
    accountNumber: str


query = gql(
    """
    mutation CreatePaymentRequest(
      $amount: MoneyInput!,
      $payerReference: String!,
      $beneficiaryReference: String!,
      $externalReference: String,
      $beneficiary: BeneficiaryInput!,
    ) {
      clientPaymentInitiationRequestCreate(
        input: {
          amount: $amount,
          payerReference: $payerReference,
          beneficiaryReference: $beneficiaryReference,
          externalReference: $externalReference,
          beneficiary: $beneficiary,
        }
      ) {
        paymentInitiationRequest {
          id
          url
        }
      }
    }
    """,
)
