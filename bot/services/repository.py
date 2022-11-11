import random

import asyncpgx

from typing import List
from sqlalchemy import select, delete, update
from sqlalchemy.dialects.postgresql import insert

from models.schemas import User, Role


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn, logger):
        self.conn = conn
        self.logger = logger

    async def list_users_str(self) -> List[int]:
        """List all bot users with balance"""
        res = self.conn.execute(select(User))
        res = res.all()
        res = [(i[0].name, i[0].role_id, i[0].birth) for i in res]

        return res

    async def get_any_role_id(self):
        roles = self.conn.execute(select(Role))
        roles = roles.all()
        rand = 0
        if len(roles) > 0:
            rand = random.randint(0, len(roles) - 1)
            return roles[rand][0].id
        else:
            return None
