"""create tables

Revision ID: a38b5821c9b8
Revises:
Create Date: 2022-05-04 12:23:22.825338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a38b5821c9b8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    category_table = op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=45), nullable=False),
    sa.Column('description', sa.String(length=90), nullable=False),
    sa.Column('created_by', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=70), nullable=False),
    sa.Column('phone', sa.String(length=14), nullable=False),
    sa.Column('cpf', sa.String(length=14), nullable=True),
    sa.Column('birthdate', sa.DateTime(), nullable=True),
    sa.Column('password_hash', sa.String(length=511), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('password_hash'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('budget',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('month_year', sa.String(), nullable=False),
    sa.Column('max_value', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expense',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=45), nullable=False),
    sa.Column('description', sa.String(length=45), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('budget_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['budget_id'], ['budget.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.bulk_insert(category_table,
        [
            {
                'name':'Food',
                'description': 'Food related expenses',
                'created_by': 'ADM'
            },
            {
                'name':'Entertainment',
                'description': 'Entertainment related expenses',
                'created_by': 'ADM'
            },
            {
                'name':'Transport',
                'description': 'Transport related expenses',
                'created_by': 'ADM'
            },
            {
                'name':'Home',
                'description': 'Home related expenses',
                'created_by': 'ADM'
            },
            {
                'name':'Health',
                'description': 'Health related expenses',
                'created_by': 'ADM'
            },
        ]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('expense')
    op.drop_table('budget')
    op.drop_table('user')
    op.drop_table('category')
    # ### end Alembic commands ###
