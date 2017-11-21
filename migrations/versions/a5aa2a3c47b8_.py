"""empty message

Revision ID: a5aa2a3c47b8
Revises: a2ea78675247
Create Date: 2017-11-21 12:27:46.007781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5aa2a3c47b8'
down_revision = 'a2ea78675247'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('chapter_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'event', 'chapter', ['chapter_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.drop_column('event', 'chapter_id')
    # ### end Alembic commands ###
