from .base import Base

from typing import List, Optional, Any, Dict
from pydantic import Field


class ParsedLogEventsDataItem(Base):
    tx_hash: str
    block_height: int
    decoded: dict


class ParsedDataItem(Base):
    tx_hash: str
    successful: bool
    block_height: int
    from_address: str
    to_address: str
    value: str
    pretty_value_quote: str
    log_events: List[ParsedLogEventsDataItem] = []


class TransactorParsedData(Base):
    address: str
    chain_name: str
    chain_id: int
    items: List[ParsedDataItem] = []


class SendTransactionNativeModel(Base):
    mainnet: str
    from_address: str
    to_address: str
    amount: int


class SendTransactionModel(Base):
    mainnet: str
    contract_address: str
    from_address: str
    to_address: str
    amount: int


class TransactionStatusModel(Base):
    status: bool
