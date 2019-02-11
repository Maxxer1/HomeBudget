"""account_id in expense and income

Revision ID: ae9cbacc0b5b
Revises: 590282626a56
Create Date: 2019-02-11 13:56:35.666118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae9cbacc0b5b'
down_revision = '590282626a56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('expense', sa.Column('account_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'expense', 'account', ['account_id'], ['id'])
    op.add_column('income', sa.Column('account_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'income', 'account', ['account_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'income', type_='foreignkey')
    op.drop_column('income', 'account_id')
    op.drop_constraint(None, 'expense', type_='foreignkey')
    op.drop_column('expense', 'account_id')
    # ### end Alembic commands ###
