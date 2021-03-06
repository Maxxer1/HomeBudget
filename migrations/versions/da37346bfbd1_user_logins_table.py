"""user_logins table

Revision ID: da37346bfbd1
Revises: bdc8da689e29
Create Date: 2019-02-04 20:53:13.226306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da37346bfbd1'
down_revision = 'bdc8da689e29'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_logins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('ip', sa.String(length=16), nullable=True),
    sa.Column('location', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_logins_ip'), 'user_logins', ['ip'], unique=False)
    op.create_index(op.f('ix_user_logins_location'), 'user_logins', ['location'], unique=False)
    op.create_index(op.f('ix_user_logins_timestamp'), 'user_logins', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_logins_timestamp'), table_name='user_logins')
    op.drop_index(op.f('ix_user_logins_location'), table_name='user_logins')
    op.drop_index(op.f('ix_user_logins_ip'), table_name='user_logins')
    op.drop_table('user_logins')
    # ### end Alembic commands ###
