from flask import Blueprint
from MyFinance.utils.voucher import VoucherUtils
from MyFinance.auth import login_required

bp = Blueprint('voucher', __name__, url_prefix='/voucher')

@bp.route("<int:voucher_number>", methods=['GET'] ) # type: ignore
def get_voucher(voucher_number):
    return VoucherUtils.get_voucher(voucher_number)

@bp.route('/')
@login_required
def enter_voucher():
    """route /voucher -- create a voucher entry

    Returns:
        renders voucher_entry.html 
    """
    return VoucherUtils.enter_voucher()

@bp.route("/voucher_result", methods=['POST', 'GET'])  # type: ignore
def voucher_result():
    return VoucherUtils.voucher_result()

@bp.route("/detail_entry", methods=['POST'])
@bp.route("/detail_entry/<int:voucher_number>/<int:split_seq_number>", methods=['GET']) # type: ignore
@login_required
def detail_entry(voucher_number=None, split_seq_number=None):
    return VoucherUtils.detail_entry(voucher_number, split_seq_number)

@bp.route("/detail_result", methods = ['POST']) # type: ignore
def detail_result():
    return VoucherUtils.detail_result()

### Deprecate in favor of search.py
@bp.route("/search", methods = ['POST']) # type: ignore
def search():
    return VoucherUtils.search()