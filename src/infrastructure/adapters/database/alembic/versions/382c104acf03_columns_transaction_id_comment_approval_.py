"""columns transaction_id comment_approval level_approval at product model

Revision ID: 382c104acf03
Revises: 777cce01a954
Create Date: 2023-01-27 10:50:34.190941

"""
from alembic import op
import sqlalchemy as sa
# Import to no generate error in migrations
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '382c104acf03'
down_revision = '777cce01a954'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('transaction_id', sa.String(length=500), nullable=True, comment='Field is filled when seller publish a product in the blockchain'))
    op.add_column('products', sa.Column('comment_approval', sa.String(length=350), nullable=True, comment='Comment by admin when approve product. This comment is sent like notification to seller user'))
    op.add_column('products', sa.Column('level_approval', sa.Integer(), nullable=True, comment='Level approved (1, 2, 3) by admin. Depending for certifications'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'level_approval')
    op.drop_column('products', 'comment_approval')
    op.drop_column('products', 'transaction_id')
    # ### end Alembic commands ###
