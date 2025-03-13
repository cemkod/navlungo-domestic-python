import requests
from typing import Optional
from navlungo_client.models import CreatePostRequest, CreateAddressRequest, UpdateAddressRequest, GetAllAddressRequest, GetAllCarriersRequest, GetBarcodeRequest, CreateTokenRequest, UpdatePostRequest, CancelPostRequest
from pydantic import ValidationError


class NavlungoClient:
    TEST_BASE_URL = "https://test-api.navlungo.com/v2.1"
    PROD_BASE_URL = "https://domestic-api.navlungo.com/v2.1"

    def __init__(self, base_url: str = PROD_BASE_URL, api_token: Optional[str] = None):
        """
        Initializes the Navlungo API client.

        Args:
            base_url: The base URL of the Navlungo API. Defaults to the production base URL.
            api_token: The API token for authentication (optional).
        """
        self.base_url = base_url
        self.token = api_token
        self.session = requests.Session()
        if self.token:
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def _request(self, method: str, endpoint: str, data: Optional[dict] = None, headers: Optional[dict] = None):
        """
        Internal method for making API requests.

        Args:
            method: The HTTP method (GET, POST, PUT, DELETE).
            endpoint: The API endpoint to call.
            data: The request body (optional).
            headers: Additional headers (optional).

        Returns:
            The JSON response from the API.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, json=data, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")

    def create_post(self, data: dict):
        """
        Creates a new post.

        Args:
            data: The request body for creating a post.

        Returns:
            The JSON response from the API.
        """
        try:
            request_data = CreatePostRequest(**data)
            headers = {"Authorization": f"Bearer {self.token}"}
            return self._request("POST", "/post/create", data=request_data.dict(by_alias=True), headers=headers)
        except ValidationError as e:
            raise ValueError(f"Invalid request data: {e}")

    def create_address(self, data: dict):
        """
        Creates a new address.

        Args:
            data: The request body for creating an address.

        Returns:
            The JSON response from the API.
        """
        try:
            request_data = CreateAddressRequest(**data)
            return self._request("POST", "/address-book/create", data=request_data.dict(by_alias=True))
        except ValidationError as e:
            raise ValueError(f"Invalid request data: {e}")

    def update_address(self, address_id: int, data: dict):
        """
        Updates an existing address.

        Args:
            address_id: The ID of the address to update.
            data: The request body for updating the address.

        Returns:
            The JSON response from the API.
        """
        try:
            request_data = UpdateAddressRequest(**data)
            return self._request("PUT", f"/address-book/update/{address_id}", data=request_data.dict(by_alias=True))
        except ValidationError as e:
            raise ValueError(f"Invalid request data: {e}")

    def get_all_addresses(self, data: dict = {}):
         """
         Retrieves all addresses.

         Args:
             data: The request body for getting all addresses.

         Returns:
         The JSON response from the API.
         """
         try:
             request_data = GetAllAddressRequest(**data)
             return self._request("GET", "/address-book/getAll", data=request_data.dict(by_alias=True))
         except ValidationError as e:
             raise ValueError(f"Invalid request data: {e}")

    def get_address(self, address_id: int):
        """
        Retrieves an address by ID.

        Args:
            address_id: The ID of the address to retrieve.

        Returns:
            The JSON response from the API.
        """
        return self._request("GET", f"/address-book/get/{address_id}")

    def delete_address(self, address_id: int):
        """
        Deletes an address by ID.

        Args:
            address_id: The ID of the address to delete.

        Returns:
            The JSON response from the API.
        """
        return self._request("DELETE", f"/address-book/delete/{address_id}")

    def get_all_carriers(self, data: dict = {}):
        """
        Retrieves all carriers.

        Args:
            data: The request body for getting all carriers.

        Returns:
            The JSON response from the API.
        """
        try:
            request_data = GetAllCarriersRequest(**data)
            return self._request("GET", "/carrier/getAll", data=request_data.dict(by_alias=True))
        except ValidationError as e:
            raise ValueError(f"Invalid request data: {e}")

    def get_my_carriers(self, data: dict = {}):
        """
        Retrieves my carriers.

        Args:
            data: The request body for getting my carriers.

        Returns:
            The JSON response from the API.
        """
        try:
            request_data = GetAllCarriersRequest(**data)
            return self._request("GET", "/carrier/my-carriers", data=request_data.dict(by_alias=True))
        except ValidationError as e:
            raise ValueError(f"Invalid request data: {e}")

    def get_barcode(self, data: dict):
        """
        Retrieves barcode.

        Args:
            data: The request body for getting barcode.

        Returns:
            The JSON response from the API.
        """
        try:
            request_data = GetBarcodeRequest(**data)
            return self._request("POST", "/barcode/getBarcode", data=request_data.dict(by_alias=True))
        except ValidationError as e:
            raise ValueError(f"Invalid request data: {e}")

    def create_token(self, data: dict):
        """
        Creates a new token.

        Args:
            data: The request body for creating a token.

        Returns:
            The JSON response from the API.
        """
        try:
            request_data = CreateTokenRequest(**data)
            response =  self._request("POST", "/auth/api", data=request_data.dict(by_alias=True))
            self.token = response.get("data").get("access_token")
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
            return response
        except ValidationError as e:
            raise ValueError(f"Invalid request data: {e}")

    def update_post(self, data: dict):
        """
        Updates a post.

        Args:
            data: The request body for updating a post.

        Returns:
            The JSON response from the API.
        """
        try:
            request_data = UpdatePostRequest(**data)
            return self._request("POST", "/post/update", data=request_data.dict(by_alias=True))
        except ValidationError as e:
            raise ValueError(f"Invalid request data: {e}")

    def check_post(self, post_number: str):
        """
        Checks a post.

        Args:
            post_number: The post number to check.

        Returns:
            The JSON response from the API.
        """
        return self._request("GET", f"/post/check/{post_number}")

    def cancel_post(self, data: dict):
        """
        Cancels a post.

        Args:
            data: The request body for cancelling a post.

        Returns:
            The JSON response from the API.
        """
        try:
            request_data = CancelPostRequest(**data)
            return self._request("POST", "/post/cancel", data=request_data.dict(by_alias=True))
        except ValidationError as e:
            raise ValueError(f"Invalid request data: {e}")