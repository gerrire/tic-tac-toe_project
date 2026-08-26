from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from di.container import Container


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="web/templates",
        static_folder="web/static",
    )

    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
    )

    container = Container()

    app.register_blueprint(
        container.game_module
    )

    return app


if __name__ == "__main__":
    application = create_app()

    application.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )