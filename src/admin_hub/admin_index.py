from quart import Blueprint, render_template, redirect, url_for, request
from quart_auth import (
    current_user,
    login_required,
    Unauthorized,
)
from src.utils import obtain_key, update_config

admin_hub = Blueprint("admin_hub", __name__)


@admin_hub.route("/admin_hub", methods=["POST", "GET"])
@login_required
async def profile():
    if current_user.auth_id == "ADMIN":
        config_whole = obtain_key(reneder_whole=True)
        config_headers = config_whole[0]
        config_content = config_whole[1]

        if request.method == "POST":
            data = await request.form
            update_config(data=list(data.to_dict().values()))

            config_whole = obtain_key(reneder_whole=True)
            config_headers = config_whole[0]
            config_content = config_whole[1]

        return await render_template(
            "admin_hub/admin_index.html",
            config_content=zip(config_content, config_headers),
        )
    else:
        return redirect(url_for("auth.unauthorized"))


@admin_hub.errorhandler(Unauthorized)
async def redirect_to_login(*_):
    """
    zrobić podstronę informującą o braku dostępu i z możliwością przekierowania do loginu/rejestracji
    """
    return redirect(url_for("auth.unauthorized"))
