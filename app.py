from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from application.services.db_connection import DBConnection
from db.create_table import create_table


app = Flask(__name__)

@app.route("/phones/create")
@use_args({"contact_name": fields.Str(required=True), "phone_value": fields.Int(required=True)}, location="query")
def phones_create_user(args):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "INSERT INTO phones (contact_name, phone_value) VALUES (:contact_name, :phone_value);",
                {"contact_name": args["contact_name"], "phone_value": args["phone_value"]},
            )

    return "Ok"


@app.route("/phones/read-all")
def phones_read_all():
    with DBConnection() as connection:
        phones = connection.execute("SELECT * FROM phones;").fetchall()

    return "<br>".join([f'{user["phone_id"]}: {user["contact_name"]} - {user["phone_value"]}' for user in phones])


@app.route("/phones/read/<int:phone_id>")
def phones_users__read(phone_id: int):
    with DBConnection() as connection:
        user = connection.execute(
            "SELECT * " "FROM phones " "WHERE (phone_id=:phone_id);",
            {
                "phone_id": phone_id,
            },
        ).fetchone()

    return f'{user["phone_id"]}: {user["contact_name"]} >>> {user["phone_value"]}'

@app.route("/phones/update/<int:phone_id>")
@use_args({"contact_name": fields.Str(), "phone_value": fields.Int()}, location="query")
def phones_users_update(args, phone_id):
    with DBConnection() as connection:
        with connection:
            contact_name = args.get("contact_name")
            phone_value = args.get("phone_value")

            if contact_name is None and phone_value is None:
                return "Need to provide at least one argument"

            args_for_request = []

            if contact_name is not None:
                args_for_request.append("contact_name=:contact_name")
            if phone_value is not None:
                args_for_request.append("phone_value=:phone_value")

            args_2 = ", ".join(args_for_request)

            connection.execute(
                "UPDATE phones " f"SET {args_2} " "WHERE phone_id=:phone_id;",
                {
                    "phone_id": phone_id,
                    "contact_name": contact_name,
                    "phone_value": phone_value,
                },
            )

    return "Ok"


@app.route("/phones/delete_user/<int:phone_id>")
def phones_delete_user(phone_id):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "DELETE " "FROM phones " "WHERE (phone_id=:phone_id);",
                {
                    "phone_id": phone_id,
                },
            )

    return "Ok"


@app.route("/")
def hello_world():
    return "HelloWorld!"


create_table()


if __name__ == "__main__":
    app.run()
