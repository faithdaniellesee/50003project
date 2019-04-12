from flask import render_template
from app import app, db

# 400: Bad Request
@app.errorhandler(400)
def bad_request_error(error):
    return render_template('errorhandlers/400.html'), 400

# 401: Unauthorized
@app.errorhandler(401)
def unauthorised_error(error):
    return render_template('errorhandlers/401.html'), 401

# 403: Forbidden
@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errorhandlers/403.html'), 403

# 404: Not Found
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errorhandlers/404.html'), 404

# 429: Too Many Requests
# @app.errorhandler(429)
# def too_many_requests_error(error):
#     return render_template('errorhandlers/429.html'), 429

# 500: Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errorhandlers/500.html'), 500

# 502: Bad Gateway
@app.errorhandler(502)
def bad_gateway_error(error):
    db.session.rollback()
    return render_template('errorhandlers/502.html'), 502

# 503: Service Unavailable
@app.errorhandler(503)
def service_unavailable_error(error):
    db.session.rollback()
    return render_template('errorhandlers/503.html'), 503

# 504: Gateway Timeout
@app.errorhandler(504)
def timeout_error(error):
    db.session.rollback()
    return render_template('errorhandlers/504.html'), 504
