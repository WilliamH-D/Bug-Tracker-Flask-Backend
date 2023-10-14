from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.String(80))
    bugs = db.relationship('Bug', backref='project')

    def __repr__(self):
        return f"{self.name} - {self.description}"

    def jsonify(self):
        return {'name': self.name,
                'description': self.description}


class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    build_ver = db.Column(db.String(20))
    priority = db.Column(db.Integer, nullable=False)

    def convert_priority(self):
        if self.priority == 0:
            return 'High priority'
        elif self.priority == 1:
            return 'Medium priority'
        elif self.priority == 2:
            return 'Low priority'
        else:
            return 'PRIORITY_PARSE_ERROR'

    def __repr__(self):
        return f"{self.description} - {self.build_ver} - {self.convert_priority()}"

    def jsonify(self):
        return {'description': self.description,
                'project_id': self.project_id,
                'project_name': self.project.name,
                'build_ver': self.build_ver,
                'priority': self.priority}
