"""empty message

Revision ID: 9797884824e6
Revises: bd891a644c31
Create Date: 2024-05-14 02:46:52.083012

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9797884824e6'
down_revision = 'bd891a644c31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('otp', sa.String(length=6), nullable=True))
        batch_op.add_column(sa.Column('otp_expiration', sa.DateTime(), nullable=True))
        batch_op.create_unique_constraint(None, ['email'])
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('otp_expiration')
        batch_op.drop_column('otp')
        batch_op.drop_column('email')

    # ### end Alembic commands ###
