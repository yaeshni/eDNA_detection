from flask import Blueprint, request, jsonify, render_template
import os
from .utils import save_file
from .models import db, Sample, TaxonomyResult

main = Blueprint("main", __name__)

# Home page
@main.route("/")
def index():
    return render_template("index.html")

# Upload Data + Metadata
@main.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    metadata = {
        "location": request.form.get("location"),
        "sample_type": request.form.get("sample_type"),
        "collection_date": request.form.get("collection_date"),
        "depth": request.form.get("depth"),
    }

    # Save file
    filepath = save_file(file) if file else None

    # Save metadata to DB
    sample = Sample(
        location=metadata["location"],
        sample_type=metadata["sample_type"],
        collection_date=metadata["collection_date"],
        depth=metadata["depth"],
        filename=os.path.basename(filepath) if filepath else None
    )
    db.session.add(sample)
    db.session.commit()

    # TODO: Run taxonomy pipeline → store results
    # Example placeholder
    dummy_species = [
        {"species": "Escherichia coli", "kingdom": "Bacteria", "phylum": "Proteobacteria", "class_name": "Gammaproteobacteria"},
        {"species": "Homo sapiens", "kingdom": "Animalia", "phylum": "Chordata", "class_name": "Mammalia"}
    ]
    for s in dummy_species:
        result = TaxonomyResult(
            species_name=s["species"],
            kingdom=s["kingdom"],
            phylum=s["phylum"],
            class_name=s["class_name"],
            sample_id=sample.id
        )
        db.session.add(result)
    db.session.commit()

    return jsonify({"message": "Upload successful", "sample_id": sample.id})

# Get Taxonomy Results
@main.route("/taxonomy_results/<int:sample_id>", methods=["GET"])
def taxonomy_results(sample_id):
    results = TaxonomyResult.query.filter_by(sample_id=sample_id).all()
    species_list = [{"species": r.species_name, "kingdom": r.kingdom, "phylum": r.phylum, "class": r.class_name} for r in results]

    # Organize tree structure (kingdom → species)
    tree = {}
    for r in results:
        if r.kingdom not in tree:
            tree[r.kingdom] = []
        tree[r.kingdom].append(r.species_name)

    return jsonify({
        "species_list": species_list,
        "taxonomy_tree": tree,
        "total_species": len(species_list)
    })
