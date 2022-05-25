from stitch_sdk.client import Stitch
from stitch_sdk.queries.create_payment_authorisation import (
    AccountType,
    BeneficiaryType,
    LinkPayBankAccount,
    Payer,
)
from stitch_sdk.queries.create_payment_request import InstantPayBankAccount
from stitch_sdk.queries.shared_types import BankId


def example_create_payment_authorisation(client: Stitch) -> str:
    bank_account: LinkPayBankAccount = {
        'name': 'Sample Account',
        'bankId': BankId.ABSA,
        'accountNumber': '1234567890',
        'accountType': AccountType.Current,
        'beneficiaryType': BeneficiaryType.Private,
        'reference': 'TestBeneficiary',
    }
    payer: Payer = {
        'email': 'sampleuser@example.com',
        'name': 'Sample User',
        'reference': 'TestPayer',
        'phoneNumber': '27821234567',
    }

    url = client.create_payment_authorisation(bank_account, payer, 'https://localhost:8000/return')

    return url


def example_create_payment_request(client: Stitch) -> str:
    bank_account: InstantPayBankAccount = {
        'name': 'Sample Account',
        'bankId': BankId.ABSA,
        'accountNumber': '1234567890',
    }
    payer: Payer = {
        'email': 'sampleuser@example.com',
        'name': 'Sample User',
        'reference': 'TestPayer',
        'phoneNumber': '27821234567',
    }

    url = client.create_payment_request(
        amount={'currency': 'ZAR', 'quantity': '123.32'},
        payer_reference='Test Ref',
        beneficiary_reference='Ben Ref',
        external_reference='Ext Ref',
        bank_account=bank_account,
        redirect_url='https://localhost:8000/return',
    )

    return url


def main():
    client = Stitch(
        url='https://api.stitch.money/graphql',
        cert_path='./certificate.pem',
        client_id='test-1111111-1111-1111-1111-1111111111',
    )

    payment_auth_url = example_create_payment_authorisation(client)
    payment_request_url = example_create_payment_request(client)

    print(payment_auth_url)
    print(payment_request_url)


if __name__ == '__main__':
    main()
