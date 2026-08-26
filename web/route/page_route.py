from flask import Blueprint, render_template


def register_page_routes(
    blueprint: Blueprint,
) -> None:

    @blueprint.get("/")
    def index():
        return render_template("index.html")