from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Market(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    # intro = db.Column(db.String(100),nullable=False)
    # text = db.Column(db.String(350),nullable=False)
    # manufacturer = db.Column(db.String(100),nullable=True)
    # country = db.Column(db.String(100),nullable=False)
    # size = db.Column(db.Integer,nullable = False)
    # wt = db.Column(db.Integer,nullable = False)
    # colour = db.Column(db.String(100),nullable = False)
    # delivery_time = db.Column(db.Integer,nullable = False)
    # material = db.Column(db.String(100),nullable = False)
    price = db.Column(db.Integer,nullable=False)
    isActive = db.Column(db.Boolean,default=True)

    def __repr__(self):
        return self.title

@app.route('/')
def home():
    markets = Market.query.order_by(Market.price).all()
    return render_template('home.html',data=markets)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/buy/<int:id>')
def buy(id):
    buy2 = Market.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "BYN",
        "amount": str(buy2.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

@app.route('/create',methods=['POST','GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        # intro = request.form['intro']
        # text = request.form['text']
        # manufacturer = request.form['manufacturer']
        # country = request.form['country']
        # wt = request.form['wt']
        # delivery_time = request.form['delivery_time']
        # material = request.form['material']

        market = Market(title=title,price=price)

        try:
            db.session.add(market)
            db.session.commit()
            return redirect('/')
        except:
            return "Произошла ошибка"

    else:
        return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()
