from flask import Blueprint, request
from database.models import Project, Bug, db
from blueprints.bugs import delete_bug

bp = Blueprint('projects', 'projects', url_prefix='/projects')


@bp.route('/')
def get_projects():
    projects = Project.query.all()
    output = []
    for project in projects:
        output.append(project.jsonify())
    return {'projects': output}


@bp.route('/<project_id>')
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    bugs = Bug.query.filter_by(project_id=project_id).all()
    bugs_output = []
    for bug in bugs:
        bugs_output.append(bug.jsonify())
    return {'project': project.jsonify(),
            'bugs': bugs_output}


@bp.route('/', methods=['POST'])
def add_project():
    project = Project(name=request.json['name'],
                      description=request.json['description'])
    db.session.add(project)
    db.session.commit()
    return {'id': project.id}


@bp.route('/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    json = project.jsonify()
    bugs = Bug.query.filter_by(project_id=project_id).all()
    bugs_output = []
    for bug in bugs:
        bugs_output.append(bug.jsonify())
        delete_bug(bug.id)
    db.session.delete(project)
    db.session.commit()
    return {'message': 'Successfully deleted',
            'project': json,
            'bugs': bugs_output}
