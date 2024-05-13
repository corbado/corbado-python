from flask import Flask, Response, jsonify, redirect, request

from corbado_python_sdk import Config, CorbadoSDK
from corbado_python_sdk.entities.user_entity import UserEntity
from corbado_python_sdk.generated.models.user_get_rsp import UserGetRsp
from corbado_python_sdk.services.interface.session_interface import SessionInterface

app = Flask(__name__)

# use your api secrets here
config: Config = Config(project_id="pro-1234", api_secret="corbado1_1234")
sdk = CorbadoSDK(config=config)


@app.route("/")
def index():
    """Root."""
    return "Hello world!"


@app.route("/setCookie")
def set_cookie() -> Response:
    """Set Cookie.

    Returns:
        Response: Response
    """
    # You'll have to supply your own short session cookie value here.
    # Bear in mind that the short session cookie value is only valid for 15 minutes.
    # If you change the cookie name via config.setShortSessionCookieName, you'll
    # have to update the cookie name here as well.
    response = Response("Cookie set!")
    response.set_cookie(
        "cbo_short_session",
        value="""eyJhbGciOiJSUzI1NiIsImtpZCI6InBraS04OTc5Mjk2NzI3NDc1MTEzNjI1IiwidHlwIjoiSldUIn0.
        eyJpc3MiOiJodHRwczovL2F1dGguY29yYmFkby5jb20iLCJzdWIiOiJ1c3ItNDE3MzM2NDA0Nzk1ODI5NDI5MSIsI
        mV4cCI6MTcxNDEzOTQyOCwibmJmIjoxNzE0MTM1ODE4LCJpYXQiOjE3MTQxMzU4MjgsImp0aSI6InRpSGdVVjMyR
        nR0d2REVk1lRm5zSHJQR3JyWjhvSiIsIm9yaWciOiJzYW50ZXkzQGdtYWlsLmNvbSIsImVtYWlsIjoic2FudGV5M0BnbWFpbC5jb20iLCJ2ZXJzaW9uIjoyfQ.
        TbEv0hWE8baPxIwHmyh822QJUR0hI4Kt83u8tOIVNaGeVHOFtrjxEAf68UwKzWwQ9_wXQiX-9uLJhz7MNEA-MXoZON
        WmOhm5yya4irIGKgcwqOQk32oONkiZdqbiUDmf2nU6slccurYEnWkamlk9BtopRZWLDR7Vwzkv3T6w5uOIG7LxKDzL5
        mwa1C9r9dhByhLxVBYjjXvqiHX8rWLA1H5awBBEnEcumM6yINAqCkv9ILsx_FSlAfoTw_mb8GoshgWl_Rlra26-eFj
        t5z35k8vjBi__mUpF4gHFRn3HFRPZri_jGLXD537KyTWevqxTTBDxopxquHqTMJTne0D44g""",
        max_age=900000,
        httponly=True,
    )
    return response


@app.route("/logged-in")
def logged_in():
    """Validate short term session.

    Returns:
        _type_: Response
    """
    try:
        short_session: str = request.cookies.get(key="cbo_short_session", default="")
        session_interface: SessionInterface = sdk.session_interface
        user: UserEntity = session_interface.get_current_user(short_session=short_session)
        if user.authenticated:
            # User is authenticated
            response_data: dict[str, str] = {
                "message": "User is authenticated!",
                "user_id": user.user_id,
                "user_name": user.name,
                "user_email": user.email,
                "user_phone_number": user.phone_number,
            }

            # Fetch additional user data
            response: UserGetRsp = sdk.user_interface.get(user_id=user.user_id)
            response_data["user_created"] = response.data.created
            response_data["user_updated"] = response.data.updated
            response_data["user_status"] = response.data.status

            return jsonify(response_data)
            # User is not authenticated, redirect to login page
        return redirect("/login", code=302)
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    app.run()
