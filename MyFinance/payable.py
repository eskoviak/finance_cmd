from MyFinance.utils.payable import PayableUtils
from flask import Blueprint
from MyFinance.auth import login_required

bp = Blueprint('payable', __name__, url_prefix='/payable')

@bp.route('<int:payable_id>', methods=['GET']) #type: ignore
@login_required
def get_payable(payable_id):
    return PayableUtils.get_payable(payable_id)
            
@bp.route('/') #type: ignore
def enter_payable():
    """/payable enter a payable

    Enter the data for a payable

    """
    return PayableUtils.enter_payable()

@bp.route('/edit/<int:payable_id>', methods=['POST', 'GET']) #type: ignore
def edit_payable(payable_id):
    return PayableUtils.edit_payable(payable_id)

@bp.route('/list/<int:vendor_number>', methods=['GET']) #type: ignore
def get_payable_by_vendor(vendor_number : int):
    """gets a list of payables by vendor
    
    <param vendor_number> : 
    """
    return PayableUtils.get_payable_by_vendor(vendor_number)


@bp.route('payable_result', methods=['POST', 'GET']) #type: ignore
def payable_result():
    """/payable/payable_result

    Target of the form on payable_entry.html
    """
    return PayableUtils.payable_result()