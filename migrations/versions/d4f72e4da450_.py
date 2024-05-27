"""empty message

Revision ID: d4f72e4da450
Revises: 9797884824e6
Create Date: 2024-05-14 04:42:37.291890

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd4f72e4da450'
down_revision = '9797884824e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('otp_expiration',
               existing_type=mysql.DATETIME(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('otp_expiration',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=True)

    # ### end Alembic commands ###
