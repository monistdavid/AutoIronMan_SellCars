from flask import Flask, render_template


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.update(
        broker='redis://localhost:6379',
        result_backend='redis://localhost:6379'
    )

    # auth the blueprint
    from view import all_bp
    for bp in all_bp:
        app.register_blueprint(bp)
    return app


sellCarsApp = create_app()
sellCarsApp.secret_key = "monist"

if __name__ == '__main__':
    sellCarsApp.run(host='0.0.0.0', port=8000)
