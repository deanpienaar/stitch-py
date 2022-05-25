from enum import Enum
from typing import TypedDict


class BankId(str, Enum):
    ABSA = 'absa'
    Capitec = 'capitec'
    Discovery = 'discovery_bank'
    FNB = 'fnb'
    Investec = 'investec'
    Nedbank = 'nedbank'
    StandardBank = 'standard_bank'
    TymeBank = 'tymebank'
    ZAAccessBank = 'za_access_bank'
    AccessBank = 'access_bank'
    FirstBankOfNigeria = 'first_bank_of_nigeria'
    GTBank = 'gtbank'
    ProvidusBank = 'providus_bank'
    SterlingBank = 'sterling_bank'
    UnitedBankForAfrica = 'united_bank_for_africa'
    VFDMicrofinanceBank = 'vfd_microfinance_bank'
    WemaBank = 'wema_bank'
    ZenithBank = 'zenith_bank'


class Currency(TypedDict):
    quantity: str
    currency: str
