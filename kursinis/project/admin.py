from flask_admin import Admin
from flask import abort
from flask_admin.contrib.sqla import ModelView
from . import db
from flask_login import login_required, current_user
from project.models import User,User_Info, Item, Cart, Item_Type, Cart_Items, Orders, Order_Items, Reviews


admin = Admin()

class Controller(ModelView):
	def is_accesible(self):
		return current_user.is_authenticated

admin.add_view(Controller(Item_Type, db.session))
admin.add_view(Controller(Item, db.session))
admin.add_view(Controller(Cart_Items, db.session))
admin.add_view(Controller(Cart, db.session))
admin.add_view(Controller(Order_Items, db.session))
admin.add_view(Controller(Orders, db.session))
admin.add_view(Controller(User, db.session))
admin.add_view(Controller(User_Info, db.session))
admin.add_view(Controller(Reviews, db.session))

