from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Text, DateTime, CHAR, Numeric
from sqlalchemy import ForeignKey
from datetime import datetime, timezone
from uuid import UUID, uuid4
from decimal import Decimal
from src.db.base import Base
from sqlalchemy.dialects.postgresql import UUID as uuid


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(uuid(as_uuid=True), primary_key=True, default=uuid4)

    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    password_hash: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    wallets: Mapped[list['Wallet']] = relationship(back_populates='user', cascade='all, delete-orphan')


class Wallet(Base):
    __tablename__ = 'wallets'

    id: Mapped[UUID] = mapped_column(uuid(as_uuid=True), primary_key=True, default=uuid4)

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                                                 nullable=False)

    user: Mapped['User'] = relationship(back_populates='wallets')

    ledger_entries: Mapped[list['LedgerEntry']] = relationship(back_populates='wallet',
                                                               order_by='LedgerEntry.created_at')


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[UUID] = mapped_column(uuid(as_uuid=True), primary_key=True, default=uuid4)

    type: Mapped[str] = mapped_column(Text, nullable=False)  # transfer, deposit, withdraw

    status: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    ledger_entries: Mapped[list['LedgerEntry']] = relationship(back_populates='transaction')


class LedgerEntry(Base):
    __tablename__ = 'ledger_entries'

    id: Mapped[UUID] = mapped_column(uuid(as_uuid=True), primary_key=True, default=uuid4)

    wallet_id: Mapped[UUID] = (mapped_column(uuid(as_uuid=True), ForeignKey('wallets.id', ondelete="RESTRICT"),
                                             nullable=False))

    transaction_id: Mapped[UUID] = (mapped_column(uuid(as_uuid=True), ForeignKey('transactions.id',
                                                                                 ondelete="RESTRICT"), nullable=False))

    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                                                 nullable=False)

    wallet: Mapped['Wallet'] = relationship(back_populates='ledger_entries')

    transaction: Mapped['Transaction'] = relationship(back_populates='ledger_entries')
