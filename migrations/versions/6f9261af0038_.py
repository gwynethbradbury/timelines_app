"""empty message

Revision ID: 6f9261af0038
Revises: 7681447dcb15
Create Date: 2017-11-29 19:42:32.881458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f9261af0038'
down_revision = '7681447dcb15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chapter', sa.Column('number', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chapter', 'number')
    # ### end Alembic commands ###
