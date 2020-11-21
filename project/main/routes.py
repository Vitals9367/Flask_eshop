from flask import Blueprint,render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from project.models import Item, Cart, Item_Type,Defined_Items, Cart_Items, Orders, Order_Items, Reviews
from project.main.forms import AddToCart, WriteReview
from project import db, whooshee
import paypalrestsdk
import stripe

main = Blueprint('main',__name__, template_folder='templates',static_folder='static',static_url_path='/main/static')

pub_key = 'pk_test_y0kbNWMwHrkmLDHTTGPVSbGi00JHpiOo4u'
secret_key = 'sk_test_QrZUDZ7oiRfB7ar1c9GMewMp00wTwWj2uD'

stripe.api_key = secret_key

@main.context_processor
def inject_types():
	types = Item_Type.query.all()
	return dict(types=types)

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "Ad1nZ9jJPoj3Gvp_7h_bnGKEGFtiuHwYlYnbftyxbii0JkIfbML46o2KtvzDfAyEVo8L-cjpJhKry9dT",
  "client_secret": "EHxDcsiAx7NrFBjwufUKKw7hU29Ovba0ZOM6Fe6F86SU3TpVfmvSrl_9YYACK0M9dXKxeLw6MB7WoF1wEHxDcsiAx7NrFBjwufUKKw7hU29Ovba0ZOM6Fe6F86SU3TpVfmvSrl_9YYACK0M9dXKxeLw6MB7WoF1w" })

@main.route('/')
def index():
	items = Item.query.all()
	return render_template('main.html',title='Home',items=items)


@main.route('/price_up/<name>')
@login_required
def price_up(name):
	Item.query.order_by(Item.price.asc()).all()
	db.session.commit() 

	return redirect(url_for(name))

@main.route('/price_down/<name>')
@login_required
def price_down(name):
	Item.query.order_by(Item.price.desc()).all()
	db.session.commit() 

	return redirect(url_for(name))

@main.route('/search',methods=['GET','POST'])
def search():
	search = request.args.get('search')
	if len(search) >= 3:
		items = Item.query.whooshee_search(search, order_by_relevance=25).all()
		if search is not None:
			return render_template('search.html',title='Home',items=items,search=search)
		else:
			flash('No items found!','danger')
			return redirect(url_for('main.index'))
	else:
		flash('Please enter longer word!','danger')
		return redirect(url_for('main.index'))

@main.route('/item/<int:item_id>',methods=['POST','GET'])
def item(item_id):
	item = Item.query.filter_by(id=item_id).first_or_404()
	reviews = Reviews.query.filter_by(item_id=item_id).all()
	form = AddToCart()
	form1 = WriteReview()
	if request.method == 'POST':
		if form.validate_on_submit():
			if current_user.is_authenticated:
				defined_item = Defined_Items(item_id=item.id,size=form.size.data,amount=form.amount.data)
				db.session.add(defined_item)
				db.session.commit() 
				new_cart_item = Cart_Items(cart_id=current_user.cart.id,defined_item_id=defined_item.id)
				db.session.add(new_cart_item)
				db.session.commit() 
				flash('Item has been added to your cart!','success')
				return redirect(url_for('main.item',item_id=item_id))
			else:
				flash('Please log in!','danger')
				return redirect(url_for('auth.login'))

		if form1.validate_on_submit():
			if current_user.is_authenticated:
				rating = form1.rating.data
				content = form1.content.data
				if len(content) > 500:
					flash('Text too long','danger')
					return redirect(url_for('main.item',item_id=item_id))
				else:
					Review = Reviews(user_id=current_user.id,item_id=item_id,rating=rating,comment=content)
					db.session.add(Review)
					db.session.commit() 
					flash('Review has been written!','danger')
					return redirect(url_for('main.item',item_id=item_id))
			else:
				flash('Please log in!','danger')
				return redirect(url_for('auth.login'))
	return render_template('item.html',title='Item',item=item,form=form,form1=form1,reviews=reviews)

@main.route('/item_by_type/<int:type_id>')
def item_type(type_id):

	items = Item.query.filter_by(item_type_id=type_id).all()
	search = Item_Type.query.filter_by(id=type_id).first().name;
	return render_template('types.html',title='Item',items=items,search=search)

@main.route('/cart',methods=['POST','GET'])
@login_required
def cart():

	Cart_Items.query.order_by(Cart_Items.date_added.desc())
	citems = Cart_Items.query.filter_by(cart_id=current_user.cart.id).all()

	amount = 0
	for citem in citems:
		amount += citem.defined_item.item.price * citem.defined_item.amount

	return render_template('cart.html',title='Cart',citems=citems,amount=amount)

@main.route('/remove_frm_cart/<int:item_id>',methods=['POST','GET'])
@login_required
def remove_item(item_id):

	item = Cart_Items.query.filter_by(id=item_id).first_or_404()
	db.session.delete(item)
	db.session.commit()

	flash('Item has been removed from your cart!','danger')

	return redirect(url_for('main.cart'))

@main.route('/clear_cart')
@login_required
def clear_cart():

	items= Cart_Items.query.all()
	if len(items):
		Cart_Items.query.delete()

		db.session.commit()

		flash(' All items has been removed from your cart!','danger')


		return redirect(url_for('main.cart'))
	else:
		flash('Cart is empty!','danger')
		return redirect(url_for('main.cart'))


@main.route('/order/payment',methods=['POST'])
@login_required
def payment():

    payment = paypalrestsdk.Payment({
    "intent": "sale",
    "payer": {
        "payment_method": "paypal"},
    "redirect_urls": {
        "return_url": "http://localhost:3000/payment/execute",
        "cancel_url": "http://localhost:3000/"},
    "transactions": [{
        "item_list": {
            "items": [{
                "name": "Order #",
                "sku": "12345",
                "price": "500.00",
                "currency": "USD",
                "quantity": 1}]},
        "amount": {
            "total": "500.00",
            "currency": "USD"},
        "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@main.route('/order/execute',methods=['POST'])
@login_required
def execute():
	success = False
	payment = paypalrestsdk.Payment.find(request.form['paymentID'])
	
	if payment.execute({'payer_id' : request.form['payerID']}):
		print('Execute success!')
		success = True
	else:
		print(payment.error)

	return jsonify({'success' : success})

@main.route('/pay/<int:order_id>',methods=['POST','GET'])
@login_required
def pay(order_id):

	order = Orders.query.filter_by(id=order_id).first_or_404()
	customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
		
	charge = stripe.Charge.create(
		customer=customer.id,
		amount=int(order.price*100),
		currency='usd',
		description=f'Order#{order.id}'
		)


	order.paid = True;

	db.session.commit()

	flash('Order has been completed!','success')
	return redirect(url_for('main.orders'))

@main.route('/payment/<int:order_id>',methods=['POST','GET'])
@login_required
def order_payment(order_id):

	order = Orders.query.filter_by(id=order_id).first_or_404()

	if current_user.info.address is None:
		flash('Please add address to your profile info!','danger')
		return redirect(url_for('profile.profile_page'))

	else:

		return render_template('payment.html',order=order,pub_key=pub_key)

@main.route('/orders')
@login_required
def orders():
	
	orders = Orders.query.filter_by(user_id=current_user.id).all()
	Orders.query.order_by(Order_Items.date_added.desc())

	return render_template('orders.html',orders=orders)

@main.route('/checkout/<int:order_id>')
@login_required
def checkout(order_id):
	order = Orders.query.filter_by(id=order_id).first_or_404()

	return render_template('checkout.html',order=order)

@main.route('/make_order/<int:item_id>',methods=['POST','GET'])
@login_required
def make_order(item_id):

	items= Cart_Items.query.all()
	if len(items):
		order = Orders(user_id=current_user.id,paid=False)

		db.session.add(order)
		db.session.commit()

		order_items = Order_Items(defined_item_id=item_id,order_id=order.id)

		db.session.add(order_items)
		db.session.commit()

		amount = 0
		for item in order.order_items:
			amount += item.defined_item.item.price * item.defined_item.amount

		order.price = amount

		db.session.commit()

		return redirect(url_for('main.checkout',order_id=order.id))
	else:
		flash('Cart is empty!','danger')
		return redirect(url_for('main.cart'))

@main.route('/order_all')
@login_required
def order_all():

	items= Cart_Items.query.all()
	if len(items):
		order = Orders(user_id=current_user.id,paid=False)

		db.session.add(order)
		db.session.commit()

		amount = 0
		for item in current_user.cart.cart_items:

			amount += item.defined_item.item.price * item.defined_item.amount
			order_item = Order_Items(defined_item_id=item.defined_item.id,order_id=order.id)
			db.session.add(order_item)

		order.price = amount
		db.session.commit()
		return redirect(url_for('main.checkout',order_id=order.id))
	else:
		flash('Cart is empty!','danger')
		return redirect(url_for('main.cart'))

@main.route('/order_selected',methods=['POST','GET'])
@login_required
def order_selected():


	if request.method == 'POST':
		id_list = request.form.getlist('id')
		items= Cart_Items.query.all()
		if len(id_list):
				order = Orders(user_id=current_user.id,paid=False)

				db.session.add(order)
				db.session.commit()

				amount = 0


				for i in id_list:

					citem = Cart_Items.query.filter_by(id=i).first()
					amount += citem.defined_item.item.price * citem.defined_item.amount

					order_item = Order_Items(defined_item_id=citem.defined_item.id,order_id=order.id)

					db.session.add(order_item)
					db.session.commit()

				order.price = amount
				db.session.commit()

				return redirect(url_for('main.checkout',order_id=order.id))
		else:
			flash('You havent selected anything!','danger')
			return redirect(url_for('main.cart'))

@main.route('/cancel_order/<int:order_id>',methods=['POST','GET'])
@login_required
def cancel_order(order_id):

	order = Orders.query.filter_by(user_id=current_user.id,id=order_id).first()
	db.session.delete(order)
	db.session.commit()

	flash('Order has been removed!','danger')

	return redirect(url_for('main.orders'))