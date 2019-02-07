"""empty message

Revision ID: aff532277930
Revises: 9b2126223bff
Create Date: 2019-02-07 14:08:30.779283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aff532277930'
down_revision = '9b2126223bff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_expense_name'), 'expense', ['name'], unique=False)
    op.create_index(op.f('ix_income_name'), 'income', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_income_name'), table_name='income')
    op.drop_index(op.f('ix_expense_name'), table_name='expense')
    # ### end Alembic commands ###
