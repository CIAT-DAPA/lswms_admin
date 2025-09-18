from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required
from ormWP import Advisory  # modelo: state (unique) y languages {en, am, or}

advisories_bp = Blueprint('advisories', __name__)

STATES = ["GOOD", "WATCH", "ALERT", "SEASONAL_DRY", "NEAR_DRY"]
LANGS = [
    {'label': 'Amharic', 'value': 'am'},
    {'label': 'Afaan Oromo', 'value': 'or'},
    {'label': 'English', 'value': 'en'},
]


@advisories_bp.route('/advisories')
@login_required
def list_advisories():
    items = Advisory.objects().order_by('state')
    return render_template('advisories.html', items=items, states=STATES, langs=LANGS)


@advisories_bp.route('/advisories/add', methods=['GET', 'POST'])
@login_required
def add_advisory():
    if request.method == 'POST':
        state = request.form.get('state', '').strip()
        en = request.form.get('text_en', '').strip()
        am = request.form.get('text_am', '').strip()
        or_ = request.form.get('text_or', '').strip()

        if state not in STATES:
            flash('Invalid state', 'danger')
            return redirect('/advisories/add')

        exists = Advisory.objects(state=state).first()
        if exists:
            flash('State already exists', 'warning')
            return redirect('/advisories')

        adv = Advisory(
            state=state,
            languages={'en': en, 'am': am, 'or': or_}
        )
        adv.save()
        flash('Advisory created successfully', 'success')
        return redirect('/advisories')

    return render_template('advisories_add.html', states=STATES, langs=LANGS)


@advisories_bp.route('/advisories/edit/<string:item_id>', methods=['GET', 'POST'])
@login_required
def edit_advisory(item_id):
    adv = Advisory.objects(id=item_id).first()
    if not adv:
        flash('Advisory not found', 'danger')
        return redirect('/advisories')

    if request.method == 'POST':
        state = request.form.get('state', '').strip()
        en = request.form.get('text_en', '').strip()
        am = request.form.get('text_am', '').strip()
        or_ = request.form.get('text_or', '').strip()

        if state not in STATES:
            flash('Invalid state', 'danger')
            return redirect(f'/advisories/edit/{item_id}')

        clash = Advisory.objects(state=state, id__ne=adv.id).first()
        if clash:
            flash('Another advisory with that state already exists', 'warning')
            return redirect(f'/advisories/edit/{item_id}')

        adv.state = state
        adv.languages = {'en': en, 'am': am, 'or': or_}
        adv.save()
        flash('Advisory updated', 'success')
        return redirect('/advisories')

    vals = {
        'en': adv.languages.get('en', ''),
        'am': adv.languages.get('am', ''),
        'or': adv.languages.get('or', ''),
    }
    return render_template('advisories_edit.html', adv=adv, states=STATES, vals=vals)


@advisories_bp.route('/advisories/delete/<string:item_id>')
@login_required
def delete_advisory(item_id):
    adv = Advisory.objects(id=item_id).first()
    if not adv:
        flash('Advisory not found', 'danger')
        return redirect('/advisories')

    adv.delete()
    flash('Advisory deleted', 'success')
    return redirect('/advisories')


@advisories_bp.errorhandler(401)
def unauthorized_handler(error):
    return render_template('error.html'), 401
