"""empty message

Revision ID: 9ed29d3060dc
Revises: bcb3e39fd35e
Create Date: 2023-10-07 18:41:18.435662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9ed29d3060dc"
down_revision = "bcb3e39fd35e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("email", sa.String(), nullable=False))
        batch_op.create_unique_constraint("email", ["email"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint("email", type_="unique")
        batch_op.drop_column("email")

    # ### end Alembic commands ###
