"""remove level column from course

Revision ID: 9c88c41408a7
Revises: 9166910090e7
Create Date: 2025-01-29 15:00:55.311156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c88c41408a7'
down_revision = '9166910090e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_tags')
    op.drop_table('course_tags')
    op.drop_table('_alembic_tmp_courses')
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.drop_column('level')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('level', sa.VARCHAR(length=50), nullable=False))

    op.create_table('_alembic_tmp_courses',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=255), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=False),
    sa.Column('duration', sa.VARCHAR(length=50), nullable=False),
    sa.Column('level', sa.VARCHAR(length=50), nullable=False),
    sa.Column('status', sa.VARCHAR(length=20), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('course_tags',
    sa.Column('course_id', sa.INTEGER(), nullable=False),
    sa.Column('tag_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('course_id', 'tag_id')
    )
    op.create_table('user_tags',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('tag_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'tag_id')
    )
    # ### end Alembic commands ###
