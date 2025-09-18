from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200))
    sample_type = db.Column(db.String(100))
    collection_date = db.Column(db.String(50))
    depth = db.Column(db.String(50))
    filename = db.Column(db.String(200))  # uploaded file name
    taxonomy_results = db.relationship("TaxonomyResult", backref="sample", lazy=True)

class TaxonomyResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    species_name = db.Column(db.String(200), nullable=False)
    kingdom = db.Column(db.String(100))
    phylum = db.Column(db.String(100))
    class_name = db.Column(db.String(100))
    count = db.Column(db.Integer, default=1)
    sample_id = db.Column(db.Integer, db.ForeignKey("sample.id"), nullable=False)
