from flask import Flask, render_template, request
from flask.views import MethodView
from wtforms import Form, StringField, SubmitField

from flatmates_bill import flat


app = Flask(__name__)


# --------------------- Views ---------------------

class HomePage(MethodView):
    def get(self):
        return render_template("index.html")


class BillFormPage(MethodView):
    def get(self):
        form = BillForm()
        return render_template("bill_form_page.html", bill_form=form)


class ResultsPage(MethodView):
    def post(self):
        form = BillForm(request.form)

        # Create bill object
        bill = flat.Bill(
            amount=float(form.amount.data),
            period=form.period.data
        )

        # Create flatmate objects
        flatmate1 = flat.Flatmate(
            name=form.name1.data,
            days_in_house=float(form.days_in_house1.data)
        )

        flatmate2 = flat.Flatmate(
            name=form.name2.data,
            days_in_house=float(form.days_in_house2.data)
        )

        return render_template(
            "results.html",
            name1=flatmate1.name,
            amount1=flatmate1.pays(bill, flatmate2),
            name2=flatmate2.name,
            amount2=flatmate2.pays(bill, flatmate1)
        )


# --------------------- Form ---------------------

class BillForm(Form):
    amount = StringField("Bill Amount:", default=100)
    period = StringField("Bill Period:", default="December 2020")

    name1 = StringField("Flatmate 1 Name:", default="John")
    days_in_house1 = StringField("Days in the house:", default=20)

    name2 = StringField("Flatmate 2 Name:", default="Mary")
    days_in_house2 = StringField("Days in the house:", default=12)

    button = SubmitField("Calculate")


# --------------------- URL Routes ---------------------

app.add_url_rule("/", view_func=HomePage.as_view("home_page"))
app.add_url_rule("/bill", view_func=BillFormPage.as_view("bill_form_page"))
app.add_url_rule(
    "/results",
    view_func=ResultsPage.as_view("results_page"),
    methods=["POST"]
)


# --------------------- Run App ---------------------

if __name__ == "__main__":
    app.run(debug=True)
