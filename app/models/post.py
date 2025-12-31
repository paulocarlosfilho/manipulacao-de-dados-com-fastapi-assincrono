import sqlalchemy as sa
from ..database import metadata

post_table = sa.Table(
    "post",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("title", sa.String(150), nullable=False, unique=True),
    sa.Column("content", sa.String, nullable=False),
    sa.Column('published_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    sa.Column('published', sa.Boolean, nullable=False, default=False) 
)
