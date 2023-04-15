from MyFinance.utils.pg_utils import PgUtils

from MyFinance.models.payables import AccountsPayable

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, current_app
)
#from werkzeug.security import check_password_hash, generate_password_hash

from MyFinance.auth import login_required

bp = Blueprint('search', __name__, url_prefix='/search')
@bp.route('<str>:search_phrase>', methods=['POST']) #type: ignore
def search_objects(self, search_phrase : str):
    
    

