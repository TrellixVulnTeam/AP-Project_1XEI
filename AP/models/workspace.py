from extensions import db

workspace_list = []


def get_last_id():
    if workspace_list:
        last_workspace = workspace_list[-1]
    else:
        return 1


class Workspace(db.Model):
    __tablename__ = 'workspace'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
