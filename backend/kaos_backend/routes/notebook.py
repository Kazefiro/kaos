from flask import Blueprint, request

from kaos_backend.controllers.notebook import NotebookController
from kaos_backend.util.flask import jsonify

from kaos_model.api import Response


def build_notebook_blueprint(controller: NotebookController):
    blueprint = Blueprint('notebook', __name__)

    @blueprint.route("/notebook/<workspace>", methods=["GET"])
    @jsonify
    def notebook_list(workspace):
        return Response(
            response=controller.list_notebooks(workspace)
        )

    @blueprint.route("/notebook/<workspace>", methods=["POST"])
    @jsonify
    def notebook_create(workspace):
        user = request.args.get('user', 'default').replace('.', '')
        cpu = request.args.get('cpu', None)
        memory = request.args.get('memory', None)
        gpu = int(request.args.get('gpu', 0))
        return controller.submit_notebook(workspace, user, request.data, cpu=cpu, memory=memory, gpu=gpu)

    @blueprint.route("/notebook/<workspace>/build/<job_id>/logs", methods=["GET"])
    @jsonify
    def build_notebook_logs(workspace, job_id):
        return controller.get_build_logs(workspace, job_id)

    @blueprint.route("/notebook/<notebook_name>", methods=["DELETE"])
    @jsonify
    def notebook_remove(notebook_name):
        return controller.remove_notebook(notebook_name)

    return blueprint
