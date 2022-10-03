from datetime import datetime

from flask import url_for

from yacut import db


class URL_map(db.Model):
    """Модель для ассоциации оригинальной и короткой ссылки."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('redirect_view',
                               short_id=self.short, _external=True)
        )
