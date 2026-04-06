from flask import Blueprint
from MyFinance.utils.search import SearchUtils

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=['POST']) #type: ignore
def search_objects():
    return SearchUtils.search_objects()
