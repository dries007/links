from flask import jsonify, render_template, redirect, request, flash, url_for
from flask_login import current_user, logout_user, login_user
from werkzeug.exceptions import HTTPException, NotFound, BadRequest, Forbidden, Unauthorized, Conflict

from links import db, app
from links.forms import LoginForm, ChangePasswordForm, ProfileEditForm, AddTokenForm, AddLinkForm
from links.helpers import admin_required, login_required
from links.models import User, Token, Link


@app.errorhandler(HTTPException)
def any_error(e):
    return render_template('error.html', e=e), e.code


@app.before_request
def before_any_request():
    if not current_user.is_anonymous and not current_user.active:
        logout_user()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/i/terms')
def terms():
    return render_template('terms.html')


@app.route('/doc/api')
def doc_api():
    func_list = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith('api_'):
            func_list.append((rule.endpoint, rule.rule, app.view_functions[rule.endpoint].__doc__))
    func_list.sort(key=lambda x: x[1])
    return render_template('docs.html', rules=func_list)


@app.route('/<id>')
def redirect_url(id):
    link = Link.query.get(id)
    if link is None or not link.active:
        raise NotFound
    return redirect(link.url, code=307)


@app.route('/i/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in', 'danger')
        return redirect(request.args.get('next') or url_for('index'))
    form = LoginForm()
    if form.submit.data and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).limit(1).first()
        if user:
            if not user.is_active:
                flash('Your account is not active.', 'danger')
                return render_template('login.html', form=form)
            if user.password == form.password.data:
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                flash('Logged in!', 'success')
                return redirect(request.args.get('next') or url_for('profile'))
            flash('Login details incorrect.', 'danger')
    return render_template('login.html', form=form)


# =================================== User


@app.route('/i/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/t/', methods=['GET', 'POST'])
@login_required
def manage_tokens():
    form = AddTokenForm()
    if form.submit.data and form.validate_on_submit():
        if not Token.query.filter_by(owner=current_user, identity=form.identity.data).limit(1).first():
            token = Token(current_user, form.identity.data)
            db.session.add(token)
            db.session.commit()
            # Clears form and allows page refresh without re-submitting the form.
            return redirect(url_for('manage_tokens'))
        flash('This identity is already in use.', 'danger')
        form.identity.errors.append('This identity is already in use.')
    return render_template('tokens.html', form=form)


@app.route('/t/<token>', methods=['GET', 'POST'])
@login_required
def token(token):
    token = Token.query.filter_by(owner=current_user, identity=token).limit(1).first()
    if not token:
        raise NotFound('Token not found.')
    form = AddLinkForm()
    if form.submit.data:
        if form.validate_on_submit():
            link = Link(token, form.url.data)
            db.session.add(link)
            db.session.commit()
            # Clears form and allows page refresh without re-submitting the form.
            return redirect(url_for('token', token=token.identity))
        for k, v in form.errors.items():
            for m in v:
                flash(m, 'danger')
    return render_template('token.html', token=token, form=form)


@app.route('/i/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileEditForm(obj=current_user)
    if form.submit.data and form.validate_on_submit():
        if current_user.password == form.password.data:
            current_user.name = form.name.data
            current_user.email = form.email.data
            db.session.add(current_user)
            db.session.commit()
            flash('Profile updated!', 'success')
            return redirect(request.args.get('next') or url_for('profile'))
        flash('Password incorrect.', 'danger')
    return render_template('edit_profile.html', form=form)


@app.route('/i/passwd', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.submit.data and form.validate_on_submit():
        if current_user.password == form.current.data:
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Password changed!', 'success')
            return redirect(request.args.get('next') or url_for('profile'))
        flash('Password incorrect.', 'danger')
    return render_template('change_password.html', form=form)


@app.route('/i/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# =================================== API


@app.route('/api/<token_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def api_token(token_id):
    """
    Manipulate a token.
    GET:
        Gets the current token data.
        Return:
            Object of {id, active, identity}
    POST:
        Change one or more of the token's data fields.
        The id cannot be set, but it can be forced to change, sending any value other than the current id, including null.
        Return:
            See GET.
        Error:
            If new identity would be a duplicate:
                409 "Conflict"
    DELETE:
        Delete the token and all links owned by it.
        *Active session is required.*
        Returns:
            True
    PUT:
        Make new links owned by this token.
        Input:
            Array of strings (URLs)
        Return:
            Array of URL ids
            If a URL is invalid, the returned id will be null.
    """
    token = Token.query.get(token_id)
    if token is None:
        raise NotFound('Token not found.')
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            raise BadRequest
        if 'active' in data and token.active != data['active']:
            token.active = data['active']
        if 'identity' in data and token.identity != data['identity']:
            if Token.query.filter_by(owner=current_user, identity=data['identity']).limit(1).first():
                raise Conflict('This identity already exists.')
            token.identity = data['identity']
        if 'id' in data and token.id != data['id']:
            token.generate_id()
        db.session.add(token)
        db.session.commit()
    elif request.method == 'DELETE':
        if current_user.is_anonymous:
            raise Forbidden
        token.delete()
        return jsonify(True)
    elif request.method == 'PUT':
        data = request.get_json()
        links = []
        for url in data:
            try:
                link = Link(token, url)
                links.append(link.id)
                db.session.add(link)
            except:
                links.append(None)
        db.session.commit()
        return jsonify(links)
    return jsonify({
        'id': token.id,
        'active': token.active,
        'identity': token.identity,
    })


@app.route('/api/<token_id>/<link_id>', methods=['GET', 'POST', 'DELETE'])
def api_link(token_id, link_id):
    """
    Manipulate a link.
    GET:
        Gets the current link data.
        Return:
            Object of {id, active, url, identity}
            identity = identity of the owner token
    POST:
        Change one or more of the links's data fields.
        The id or identity cannot be changed. Sending them will be ignored.
        Return:
            See GET.
    DELETE:
        Delete the link.
        Return:
            True
    """
    token = Token.query.get(token_id)
    if token is None:
        raise Unauthorized('Token not found.')
    link = Link.query.get(link_id)
    if link is None:
        raise NotFound('Link ID not found.')
    if request.method == 'POST':
        data = request.get_json()
        if 'active' in data and link.active != data['active']:
            link.active = data['active']
        if 'url' in data and link.url != data['url']:
            link.url = data['url']
        db.session.add(link)
        db.session.commit()
    elif request.method == 'DELETE':
        link.delete()
        return jsonify(True)
    return jsonify({
        'id': link.id,
        'active': link.active,
        'url': link.url,
        'identity': token.identity,
    })

# =================================== Admin


@app.route('/i/admin')
@admin_required
def admin():
    return render_template('admin.html', users=User.query.all(), tokens=Token.query.all(), links=Link.query.all())


@app.route('/u/<user>')
@admin_required
def other_profile(user):
    user = User.query.get(user)
    if not user:
        raise NotFound('User not found.')
    return render_template('profile.html', user=user)
