from datetime import datetime, timedelta
from functools import lru_cache
from typing import Dict, List, Optional
from task1 import get_token
from requests import request
import math

DOMAIN = "https://recruitment.developers.emako.pl"


class Connector:
    @lru_cache
    def headers(self) -> Dict[str, str]:

        return {
            "Authorization": get_token(),
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def request(self, method: str, path: str, data: dict = {}, page_size=20, page_index=None) -> dict:
        if page_index is not None:
            data["pagination"] = {"page_size": page_size, "index": page_index}

        return request(
            method, f"{DOMAIN}/{path}", json=data, headers=self.headers()
        ).json()

    def get_products(self, ids: Optional[List[int]] = None, page_index=0) -> List[dict]:
        return self.request("GET", "products", {"ids": ids}, page_size=40, page_index=page_index)["result"]

    def get_all_products_summary(self, page_index=0) -> List[dict]:
        return self.request("GET", "products", {"detailed": False}, page_size=40, page_index=page_index)["result"]

    def get_new_products(self, newer_than: Optional[datetime] = None, page_index=0) -> List[dict]:
        if newer_than is None:
            newer_than = datetime.now() - timedelta(days=5)
        return self.request(
            "GET", "products", {"created_at": {"start": newer_than.isoformat()}}, page_size=40, page_index=page_index)["result"]

    def add_products(self, products: List[dict]):
        result = []

        for page_index in range(math.ceil(len(products)/20)):
            result.append(self.request("POST", "products", {"products": products[:20]})["result"])
            products = products[20:]

        return result

    def update_stocks(self, stocks: Dict[int, list]):
        current_data = self.get_products(list(stocks))
        result = []

        for page_index in range(math.ceil(len(stocks)/20)):
            for product_entry in current_data:
                product_entry["details"]["supply"] = stocks[product_entry["id"]]

            result.append(self.request("PUT", "products", {"products": current_data[:20]}))
            current_data = current_data[20:]

        return result


