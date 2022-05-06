from decimal import Decimal

from stitch.client import Stitch
from stitch.queries.create_payment_authorisation import (
    Payer, LinkPayBankAccount, BeneficiaryType, AccountType
)
from stitch.queries.create_payment_request import InstantPayBankAccount
from stitch.queries.shared_types import BankId


def main():
    client = Stitch(
        'https://api.stitch.money/graphql',
        './stitch/certificate.pem',
        'test-282cd917-4a42-4ddc-9e59-ddc2df985896',
    )

    bank_account: InstantPayBankAccount = {
        'name': 'Sample Account',
        'bankId': BankId.ABSA,
        'accountNumber': '1234567890',
        # 'accountType': AccountType.Current,
        # 'beneficiaryType': BeneficiaryType.Private,
        # 'reference': 'TestBeneficiary'
    }
    payer: Payer = {
        'email': 'sampleuser@example.com',
        'name': 'Sample User',
        'reference': 'TestPayer',
        'phoneNumber': '27821234567'
    }

    x = client.create_payment_request(
        amount={'currency': 'ZAR', 'quantity': '123.32'},
        payer_reference='Test Ref',
        beneficiary_reference='Ben Ref',
        external_reference='Ext Ref',
        bank_account=bank_account,
    )

    print(x)


if __name__ == '__main__':
    main()
