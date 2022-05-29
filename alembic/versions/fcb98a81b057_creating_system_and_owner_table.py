"""Creating system and Owner table

Revision ID: fcb98a81b057
Revises: 
Create Date: 2022-05-29 15:30:59.098394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcb98a81b057'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'owner',sa.Column('id',sa.Integer(),autoincrement = True,primary_key = True,nullable = False),
        sa.Column('username',sa.String(),nullable = False,unique = True),
        sa.Column('email',sa.String(),nullable = False,unique = True),
        sa.Column('password',sa.String(),nullable = False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable = False,server_default = sa.text('now()'))
    )
    op.create_table(
        'System',
        sa.Column('id',sa.Integer(),nullable = False,primary_key = True,autoincrement = True),
        sa.Column('name',sa.String(),nullable = False),
        sa.Column('added_at',sa.TIMESTAMP(timezone=True),nullable = False,server_default = sa.text('now()')),
        sa.Column('ownerid',sa.Integer(),sa.ForeignKey('owner.id',ondelete="CASCADE"),nullable = False),
        sa.Column('in_user',sa.Boolean,nullable = False,server_default = 'False')
    )
    
    op.create_table(
        'user',
        sa.Column('name',sa.String(),nullable = False),
        sa.Column('phone',sa.String(length=10),nullable = False,primary_key = True),
        sa.Column('system_id',sa.Integer(),sa.ForeignKey('System.id',ondelete="CASCADE"),nullable = False)
    )
    op.create_table(
        'History',
        sa.Column(
            'systemid',
            sa.Integer(),
            sa.ForeignKey('System.id',
                          ondelete="CASCADE"),
            primary_key = True,
            nullable = False,
        ),
        sa.Column(
            'phone',
            sa.String(length=10),
            sa.ForeignKey(
                'user.phone',
                ondelete="CASCADE"
            ),
            nullable = False,
            primary_key = True
        )
    )

def downgrade():
    op.drop_table('History')
    op.drop_table('user')
    op.drop_table('System')
    op.drop_table('owner')
