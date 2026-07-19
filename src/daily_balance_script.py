from sqlalchemy import update, select, exists
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dtos.schemas import ClientUpdateSchema
from src.core.clients.update_client import update_vpn_client
from src.repos.database.models import ClientModel, UserModel

from sqlalchemy import update, select, exists
from sqlalchemy.ext.asyncio import AsyncSession


async def run_daily_billing(session: AsyncSession, daily_cost: int = 10):
    async with session.begin():
        has_active_client = exists().where(
            ClientModel.tg_id == UserModel.tg_id,
            ClientModel.enable == True
        )

        balance_minimized = await session.execute(
            update(UserModel)
            .where(has_active_client)
            .values(balance=UserModel.balance - daily_cost)
        )

        if balance_minimized.rowcount > 0:
            zero_balance_users = select(UserModel.tg_id).where(UserModel.balance <= 0)

            turned_off = await session.execute(
                update(ClientModel)
                .where(ClientModel.tg_id.in_(zero_balance_users))
                .values(enable=False)
                .returning(ClientModel.email)
            )

            disabled_emails = turned_off.scalars().all()

            if disabled_emails:
                for email in disabled_emails:
                    await update_vpn_client(
                        email=email,
                        updated_client=ClientUpdateSchema(
                            enable=False
                        )
                    )
            



