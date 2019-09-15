from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """
    Function for handling 404 not found errors.
    Renders a 404 template.

    Args:
        error: Error code.

    Returns:
        object: Returns a template object.
    """
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    """
    Function for handling 403 not found errors.
    Renders a 404 template.

    Args:
        error: Error code.

    Returns:
        object: Returns a template object.
    """
    return render_template('errors/403.html'), 403
