"""created table user

Revision ID: 675c573f957b
Revises: 
Create Date: 2022-04-28 14:28:55.277930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '675c573f957b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=70), nullable=False),
    sa.Column('phone', sa.String(length=14), nullable=False),
    sa.Column('cpf', sa.String(length=14), nullable=True),
    sa.Column('birthdate', sa.Date(), nullable=True),
    sa.Column('password_hash', sa.String(length=511), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('password_hash'),
    sa.UniqueConstraint('phone')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###