"""Updated Course table

Revision ID: c833af4c1f55
Revises: fe8161571baf
Create Date: 2022-10-24 17:39:55.471273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c833af4c1f55'
down_revision = 'fe8161571baf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('courses_user_id_fkey', 'courses', type_='foreignkey')
    op.drop_column('courses', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courses', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('courses_user_id_fkey', 'courses', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
