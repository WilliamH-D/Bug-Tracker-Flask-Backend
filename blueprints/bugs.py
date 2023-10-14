from flask import Blueprint, request
from database.models import Project, Bug, db

bp = Blueprint('bugs', 'bugs', url_prefix='/bugs')


@bp.route('/')
def get_bugs():
    bugs = Bug.query.all()
    output = []
    for bug in bugs:
        output.append(bug.jsonify())
    return {'bugs': output}


@bp.route('/<bug_id>')
def get_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    return bug.jsonify()


@bp.route('/', methods=['POST'])
def add_bug():
    project_id = request.json['project_id']
    project = Project.query.get(project_id)
    if project is None:
        return {'error': 'Could not find project with ID ' + str(project_id)}
    bug = Bug(description=request.json['description'],
              project_id=project_id,
              build_ver=request.json['build_ver'],
              priority=request.json['priority'])
    db.session.add(bug)
    db.session.commit()
    return {'id': bug.id}


@bp.route('/<bug_id>', methods=['DELETE'])
def delete_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    json = bug.jsonify()
    db.session.delete(bug)
    db.session.commit()
    return {'message': 'Successfully deleted',
            'bug': json}
