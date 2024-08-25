from .base import Base
from typing import Optional, List


class ParsedDataItem(Base):
    logo_url: Optional[str]
    contract_display_name: Optional[str]
    quote: float = 0
    pretty_quote: Optional[str]
    balance: int = 0


class CheckerParsedData(Base):
    address: Optional[str]
    chain_name: Optional[str]
    chain_id: int = 0
    quote_currency: Optional[str]
    items: List[ParsedDataItem]
