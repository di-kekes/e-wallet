from decimal import Decimal
from src.db.models import User, Transaction, LedgerEntry, Wallet
from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy import select, func


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> None:
        self.session.add(user)

    def get(self, user_id: UUID) -> User | None:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.session.query(User).filter_by(email=email).one_or_none()

    def get_all_users(self) -> list[User]:
        return list(self.session.scalars(select(User)).all())

    def delete_user(self, user: User) -> None:
        self.session.delete(user)


class WalletRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, wallet: Wallet) -> None:
        self.session.add(wallet)

    def get_by_id(self, wallet_id: UUID) -> Wallet | None:
        return self.session.get(Wallet, wallet_id)

    def get_all_wallets(self) -> list[Wallet]:
        return list(self.session.scalars(select(Wallet)).all())

    def get_balance(self, wallet_id: UUID) -> Decimal:
        stmt = select(func.coalesce(func.sum(LedgerEntry.amount), 0)).where(LedgerEntry.wallet_id == wallet_id)
        return self.session.execute(stmt).scalar_one()

    def get_all_wallets_of_user(self, user_id: UUID) -> list[Wallet]:
        stmt = select(Wallet).where(Wallet.user_id == user_id)
        return list(self.session.execute(stmt).scalars().all())

    def delete_wallet(self, wallet: Wallet) -> None:
        self.session.delete(wallet)


class TransactionRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, transaction: Transaction) -> None:
        self.session.add(transaction)

    def get_by_id(self, transaction_id: UUID) -> Transaction | None:
        return self.session.get(Transaction, transaction_id)

    def delete_transaction(self, transaction: Transaction):
        self.session.delete(transaction)


class LedgerEntryRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, ledger_entry: LedgerEntry):
        self.session.add(ledger_entry)

    def delete_ledger_entry(self, ledger_entry: LedgerEntry):
        self.session.delete(ledger_entry)

    def get_all_for_wallet(self, wallet_id: UUID) -> list[LedgerEntry]:
        stmt = select(LedgerEntry).where(LedgerEntry.wallet_id == wallet_id).order_by(LedgerEntry.created_at)
        return list(self.session.execute(stmt).scalars().all())
