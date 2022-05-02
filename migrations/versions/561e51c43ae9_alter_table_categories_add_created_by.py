"""alter table categories add created_by

Revision ID: 561e51c43ae9
Revises: ef5154b628dd
Create Date: 2022-05-02 03:07:11.453735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '561e51c43ae9'
down_revision = 'ef5154b628dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('created_by', sa.String(length=20), nullable=False))
    op.execute(
        "INSERT INTO \
            category (name, description, created_by) \
         VALUES \
             ('Food', 'Food related expenses', 'ADM'),\
             ('Entertainment', 'Entertainment related expenses', 'ADM'),\
             ('Transport', 'Transport related expenses', 'ADM'),\
             ('Home', 'Home related expenses', 'ADM'),\
             ('Health', 'Health related expenses', 'ADM')"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category', 'created_by')
    # ### end Alembic commands ###
