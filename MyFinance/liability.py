from flask import Blueprint
from MyFinance.utils.liability import LiabilityUtils

bp = Blueprint('liability', __name__, url_prefix='/liability')

@bp.route('/', methods=['GET']) #type: ignore
def enter_liability():
    """Ender liability:  displays the template `liability_entry.html` to capture the data for a liability (loan, long term payable).
    
    :return: none
    :rtype: none
    """
    return LiabilityUtils.enter_liability()

@bp.route('liability_result', methods=['GET', 'POST']) #type: ignore
def liability_result():
    return LiabilityUtils.liability_result()

@bp.route('<int:liability_id>', methods=['GET']) #type: ignore
def get_liability(liability_id):
    return LiabilityUtils.get_liability(liability_id)

@bp.route('/liability/<int:account_number>', methods=['GET']) #type: ignore
def get_liabiity_list(account_number):
    return LiabilityUtils.get_liabiity_list(account_number)