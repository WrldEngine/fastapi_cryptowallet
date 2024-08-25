from lqd_services import WalletGenerator, MnemonicGenerator, Checker, Transactor


class WalletGeneratorService:

    @classmethod
    async def generate(cls) -> WalletGenerator:
        self = cls()
        self.wallet_generator = WalletGenerator(depth=1)
        self.mnemonics = await MnemonicGenerator.generate_bip39_phrase()
        self.secrets = await self.wallet_generator.generate_secrets(self.mnemonics)

        return self

    @staticmethod
    async def recover(mnemonics: str) -> WalletGenerator:
        return await WalletGenerator(depth=1).generate_secrets(mnemonics)


class CheckerService:

    @staticmethod
    async def fetch_balances(address: str, chain_name: str) -> Checker:
        return await Checker.fetch_balances(address=address, chain_name=chain_name)

    @staticmethod
    async def fetch_transactions(address: str, chain_name: str) -> Checker:
        return await Checker.fetch_transactions(address=address, chain_name=chain_name)


class TransactionService:

    @staticmethod
    async def send_native(
        mainnet: str,
        from_private_key: str,
        from_address: str,
        to_address: str,
        amount: int,
    ) -> bool:
        transactor = Transactor(chain_name=mainnet)
        return await transactor.send_native(
            from_private_key=from_private_key,
            from_address=from_address,
            to_address=to_address,
            amount=amount,
        )

    @staticmethod
    async def send_erc20(
        mainnet: str,
        contract_address: str,
        from_private_key: str,
        from_address: str,
        to_address: str,
        amount: int,
    ) -> bool:
        transactor = Transactor(chain_name=mainnet)
        return await transactor.send_erc20(
            contract_address=contract_address,
            from_private_key=from_private_key,
            from_address=from_address,
            to_address=to_address,
            amount=amount,
        )

    @staticmethod
    async def send_bep20(
        mainnet: str,
        contract_address: str,
        from_private_key: str,
        from_address: str,
        to_address: str,
        amount: int,
    ) -> bool:
        transactor = Transactor(chain_name=mainnet)
        return await transactor.send_bep20(
            contract_address=contract_address,
            from_private_key=from_private_key,
            from_address=from_address,
            to_address=to_address,
            amount=amount,
        )
