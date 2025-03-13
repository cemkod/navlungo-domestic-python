from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum

class CarrierId(Enum):
    TASIYICI_AYARLARI = 1
    SURAT_KARGO = 9
    HEPSIJET = 10
    KOLAY_GELSIN = 11
    SCOTTY = 12
    ARAS_KARGO = 13
    PTT_KARGO = 14
    VIGO = 15
    HEPSIJET_XL = 16

class BarcodeType(Enum):
    PDF = "pdf"
    HTML = "html"
    ZPL = "zpl"

class Address(BaseModel):
    addressId: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    post_code: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None

class SenderAddress(BaseModel):
    addressId: Optional[str] = None

class PostDetails(BaseModel):
    desi: float
    package_count: int
    price: Optional[str] = None
    note: Optional[str] = None

class PostItem(BaseModel):
    reference_id: str
    carrier_id: CarrierId
    post_type: int
    cod_payment_type: Optional[str] = None
    sender: SenderAddress
    recipient: Address
    post: PostDetails
    barcode_format: str
    custom_data_1: Optional[str] = None
    custom_data_2: Optional[str] = None
    custom_data_3: Optional[str] = None
    custom_data_4: Optional[str] = None

class CreatePostRequest(BaseModel):
    platform: Optional[str] = None
    posts: List[PostItem]

class CreateAddressRequest(BaseModel):
    address_type: str  # sender or recipient
    location_name: Optional[str] = None  # required for sender
    address_name: str
    address_email: Optional[str] = None
    address_phone: str
    address_line: str
    address_country: str
    address_city: str
    address_district: str
    address_post_code: Optional[str] = None
    is_main_warehouse: Optional[int] = None  # only for sender

class UpdateAddressRequest(BaseModel):
    address_type: str  # sender or recipient
    location_name: Optional[str] = None  # required for sender
    address_name: str
    address_email: Optional[str] = None
    address_phone: str
    address_line: str
    address_country: str
    address_city: str
    address_district: str
    address_post_code: Optional[str] = None
    is_main_warehouse: Optional[int] = None  # only for sender

class GetAllAddressRequest(BaseModel):
    limit: Optional[int] = 20
    page: Optional[int] = 1
    filters: Optional[Dict[str, str]] = None

class GetAllCarriersRequest(BaseModel):
    limit: Optional[int] = 20

class GetBarcodeRequest(BaseModel):
    post_number: str
    barcode_type: BarcodeType

class CreateTokenRequest(BaseModel):
    username: str
    password: str

class UpdatePostRequest(BaseModel):
    post_number: str
    sender: Optional[Address] = None
    recipient: Optional[Address] = None
    post: Optional[PostDetails] = None
    barcode_format: Optional[str] = None
    custom_data_1: Optional[str] = None
    custom_data_2: Optional[str] = None
    custom_data_3: Optional[str] = None
    custom_data_4: Optional[str] = None

class CancelPostRequest(BaseModel):
    post_number: str