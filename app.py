from flask import Flask, render_template, request, flash
import requests


app = Flask(__name__)
app.secret_key = "secret_key"


def get_exchange_rate(from_currency, to_currency, amount):
    try:
        url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        print(data)

        exchange_rate = data.get("info", {}).get("rate")
        if exchange_rate is not None:
            return exchange_rate
        else:
            raise Exception("Exchange rate not found in the response.")
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return None


def convert_currency(from_currency, to_currency, amount):
    exchange_rate = get_exchange_rate(from_currency, to_currency, amount)
    if exchange_rate is not None:
        try:
            amount = float(amount)
            converted_amount = amount * exchange_rate
            return round(converted_amount, 2)
        except ValueError:
            flash("Invalid amount. Please enter a valid number.", "error")
    return None


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        from_currency = request.form.get("from_currency")
        to_currency = request.form.get("to_currency")
        amount = request.form.get("amount")

        if not from_currency or not to_currency or not amount:
            flash("Invalid input. Please check your inputs and try again.", "error")
        else:
            result = convert_currency(from_currency, to_currency, amount)
            if result is not None:
                flash(f"{amount} {from_currency} = {result} {to_currency}", "success")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
