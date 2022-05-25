from dataclasses import dataclass, field
import time
from urllib.parse import urlencode
from uuid import uuid4 as uuid

from gql import Client
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport
from graphql import DocumentNode
import jwt
import requests

from .exceptions import StitchAPIError
from .queries import create_payment_authorisation, create_payment_request
from .queries.create_payment_authorisation import InitialPayment, LinkPayBankAccount, Payer
from .queries.create_payment_request import InstantPayBankAccount
from .queries.shared_types import Currency


@dataclass
class Stitch:
    url: str
    cert_path: str
    client_id: str

    _gql_client: Client | None = field(init=False, default=None)

    def create_payment_authorisation(
        self,
        bank_account: LinkPayBankAccount,
        payer: Payer,
        redirect_url: str,
        initial_payment: InitialPayment = None,
    ) -> str:
        result = self._make_query(
            create_payment_authorisation.query,
            variables={
                'beneficiary': {'bankAccount': bank_account},
                'payer': payer,
                'initialPayment': initial_payment,
            },
        )

        url = result['clientPaymentAuthorizationRequestCreate']['authorizationRequestUrl']

        return self._build_redirect_url(url, redirect_url)

    def create_payment_request(
        self,
        amount: Currency,
        payer_reference: str,
        beneficiary_reference: str,
        external_reference: str,
        bank_account: InstantPayBankAccount,
        redirect_url: str,
    ):
        result = self._make_query(
            create_payment_request.query,
            variables={
                'amount': amount,
                'payerReference': payer_reference,
                'beneficiaryReference': beneficiary_reference,
                'externalReference': external_reference,
                'beneficiary': {'bankAccount': bank_account},
            },
        )

        payment_request = result['clientPaymentInitiationRequestCreate']['paymentInitiationRequest']
        url = payment_request['url']

        return self._build_redirect_url(url, redirect_url)

    @property
    def gql_client(self) -> Client:
        if self._gql_client is None:
            client_token = self._get_client_token()
            auth_header = {'Authorization': f'Bearer {client_token}'}

            transport = RequestsHTTPTransport(self.url, headers=auth_header)
            client = Client(transport=transport)

            self._gql_client = client

        return self._gql_client

    def reset_auth(self):
        self._gql_client = None

    def _make_query(self, document: DocumentNode, variables: dict[str] = None) -> dict:
        try:
            return self.gql_client.execute(document, variable_values=variables)
        except TransportQueryError as error:
            stitch_error = Stitch._extract_stitch_error(error.errors)

            if stitch_error is None:
                raise error

            raise StitchAPIError(stitch_error['extensions']['code'], stitch_error['message'])

    @staticmethod
    def _extract_stitch_error(errors: list[dict[str, str]]) -> dict | None:
        for error in errors:
            if error.get('extensions', {}).get('code'):
                return error

    def _get_client_token(self) -> str:
        url = 'https://secure.stitch.money/connect/token'
        client_assertion = self._generate_client_assertion()

        response = requests.post(
            url,
            data={
                'client_id': self.client_id,
                'scope': 'client_paymentauthorizationrequest client_paymentrequest',
                'grant_type': 'client_credentials',
                'audience': url,
                'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
                'client_assertion': client_assertion,
            },
        ).json()

        return response['access_token']

    def _generate_client_assertion(self) -> str:
        with open(self.cert_path, 'r') as cert:
            secret = cert.read()

            now = int(time.time())
            one_hour_from_now = now + 3600

            payload = {
                'aud': 'https://secure.stitch.money/connect/token',
                'iss': self.client_id,
                'sub': self.client_id,
                'jti': str(uuid()),
                'iat': now,
                'nbf': now,
                'exp': one_hour_from_now,
            }

            return jwt.encode(payload, secret, algorithm='RS256')

    @staticmethod
    def _build_redirect_url(base_url: str, redirect_url: str) -> str:
        return f'{base_url}?{urlencode({"redirect_uri": redirect_url})}'
