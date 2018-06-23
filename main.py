import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)
app.secret_key = b'|\xea\xa6!\xb6EL\xc0\x06\xe9,\x94\xbc,\xbf\xc0\x7f!<!\xb7\xe9/\x12'


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Catch values submitted in the form
        input_name = str(request.form['name'])
        amount = int(request.form['amount'])

        # Save those values to the user's session
        session['name'] = input_name
        session['amount'] = amount

        # Prepare the data to be saved
        name = Donor(name=input_name)
        name.save()

        # Save the donation data to the database
        Donation(donor=name, value=amount).save()

        # Redirect the visitor to the home page.
        return redirect(url_for('all'))

    return render_template('create.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

