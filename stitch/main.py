from stitch.client import Stitch
from stitch.queries.create_payment_authorisation import (
    Payer,
    LinkPayBankAccount,
    BeneficiaryType,
    AccountType,
)
from stitch.queries.create_payment_request import InstantPayBankAccount
from stitch.queries.shared_types import BankId


def example_create_payment_authorisation(client: Stitch) -> str:
    bank_account: LinkPayBankAccount = {
        'name': 'Sample Account',
        'bankId': BankId.ABSA,
        'accountNumber': '1234567890',
        'accountType': AccountType.Current,
        'beneficiaryType': BeneficiaryType.Private,
        'reference': 'TestBeneficiary'
    }
    payer: Payer = {
        'email': 'sampleuser@example.com',
        'name': 'Sample User',
        'reference': 'TestPayer',
        'phoneNumber': '27821234567'
    }

    url = client.create_payment_authorisation(bank_account, payer, 'https://example.com')

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
        'phoneNumber': '27821234567'
    }

    url = client.create_payment_request(
        amount={'currency': 'ZAR', 'quantity': '123.32'},
        payer_reference='Test Ref',
        beneficiary_reference='Ben Ref',
        external_reference='Ext Ref',
        bank_account=bank_account,
        redirect_url='https://example.com/payment',
    )

    return url


def main():
    client = Stitch(
        url='https://api.stitch.money/graphql',
        cert_path='./stitch/certificate.pem',
        client_id='test-282cd917-4a42-4ddc-9e59-ddc2df985896',
    )

    payment_auth_url = example_create_payment_authorisation(client)
    payment_request_url = example_create_payment_request(client)


if __name__ == '__main__':
    main()
