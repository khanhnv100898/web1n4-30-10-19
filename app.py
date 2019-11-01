from bson import ObjectId
from flask import Flask, render_template, request, redirect, session
from gmail import *
from datetime import datetime
from models.product import Product
from models.login import Login
from models.order import Order
import pyexcel
from pymongo import MongoClient


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdasdasd23423@#4'

# Trang chủ
@app.route('/')
def index():
    return render_template('index.html')

# Search
# Hiển thị danh sách sản phẩm
@app.route('/search/<search>')
def search(search):
    session['search'] = search
    all_product_gender = Product.find({'product_gender': search})
    if all_product_gender is not None:
        return render_template('search/search.html', all_product=all_product_gender)
    # elif session['search'] == "Kids":
    elif search == "Kids":
        all_product_kids = Product.find({'product_kids': True})
        if all_product_kids is not None:
            return render_template('search/search.html', all_product=all_product_kids)

# Search Info Kids
@app.route('/search_kids_info')
def search_kids_info():
    product = Product.find({"product_kids": True})
    return render_template('search/search.html', all_product=product)


@app.route('/search_type/<search_type>')
def search_type(search_type):
    session['search_type'] = search_type
    all_product_type = Product.find({"product_type": search_type})
    if all_product_type is not None:
        return render_template('search/search.html', all_product=all_product_type)

# Chi tiết sản phẩm
@app.route('/product/detail/<id>')
def productDetail(id):
    product = Product.find_one({"_id": ObjectId(id)})
    return render_template('search/detail.html', detail_product=product)

# Đăng ký
@app.route('/sign_up', methods=['GET', 'POST'])
def signUp():
    if request.method == 'GET':
        return render_template('signup/signup-user.html')
    elif request.method == 'POST':
        form = request.form
        fullname = form['fullname']
        username = form['username']
        password = form['password']
        # level = form['level']
        email = form['email']
        phone = form['phone']
        address = form['address']
        id_person = form['id_person']
        balance = form['balance']

        found_login = Login.find({"username": username})
        c = int(found_login.count())
        if c > 0:
            return render_template('signup/signup-fail.html', template=1)
        else:
            new_login = {
                "fullname": fullname,
                "username": username,
                "password": password,
                "level": 2,
                "email": email,
                "phone": phone,
                "id_person": id_person,
                "address": address,
                "balance": balance,
            }
            Login.insert_one(new_login)

            found_login = Login.find_one({'username': username})
            gmail = GMail('ngovankhanh108@gmail.com', 'KhanhNgo108')
            html_content = '''
        Chúc mừng bạn đã tạo tài khoản thành công trên hệ thống.
        Cảm ơn quý khách đã sử dụng dịch vụ của chúng tôi!
        '''
            msg = Message('Tạo tài khoản thành công',
                          to=found_login['email'], html=html_content)
            gmail.send(msg)
            return redirect('/login')


# Đăng nhập phân quyền
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('logins/login-user.html')
    elif request.method == 'POST':
        form = request.form
        login_username = form['username']
        login_password = form['password']
        login = Login.find_one({'username': login_username})
        if login is None:
            return render_template('logins/login-fail.html')
        else:
            if login_password == login['password']:
                session['loggedin'] = True
                session['level_loggedin'] = str((login['level']))

                if session['level_loggedin'] == "2":
                    session["user_id"] = str(login["_id"])
                    return render_template('user.html', login=login)
                elif session['level_loggedin'] == "1":
                    session["admin_id"] = str(login["_id"])
                    return render_template('admin.html', login=login)
                elif session['level_loggedin'] == "3":
                    session["shipper_id"] = str(login["_id"])
                    return render_template('shipper.html', login=login)
            else:
                return render_template('logins/login-fail.html')

# Đăng xuất
@app.route('/logout')
def logout():
    if "loggedin" in session:
        if session['loggedin'] == False:
            return redirect('/')
        else:
            session['loggedin'] = False
            if session['level_loggedin'] == "1":
                del session['admin_id']
                del session['level_loggedin']
            elif session['level_loggedin'] == "2":
                del session['user_id']
                del session['level_loggedin']
            elif session['level_loggedin'] == "3":
                del session['shipper_id']
                del session['level_loggedin']
            return redirect('/')
    else:
        return redirect('/')


# Update thông tin đăng nhập
@app.route('/all_login/update/<id>', methods=['GET', 'POST'])
def updateLogin(id):
    login = Login.find_one({"_id": ObjectId(id)})
    if request.method == 'GET':
        return render_template('update_login.html', login=login)
    elif request.method == 'POST':
        form = request.form
        fullname = form['fullname']
        username = form['username']
        password = form['password']
        level = form['level']

        update_login = {"$set": {
            "fullname": fullname,
            "username": username,
            "password": password,
            "level": level,
        }}
        Login.update_one(login, update_login)
        return redirect('/all_login')

# Update thông tin đăng nhập User
@app.route('/update/<id>', methods=['GET', 'POST'])
def updateLoginUser(id):
    login = Login.find_one({"_id": ObjectId(id)})
    if request.method == 'GET':
        return render_template('user/user-update.html', update_user=login)
    elif request.method == 'POST':
        form = request.form
        fullname = form['fullname']
        username = form['username']
        password = form['password']
        phone = form['phone']
        email = form['email']
        address = form['address']
        # level = form['level']

        update_login = {"$set": {
            "fullname": fullname,
            "username": username,
            "password": password,
            "level": 2,
            "phone": phone,
            "email": email,
            "address": address,
        }}
        Login.update_one(login, update_login)
        return redirect('/homeLogin')

# Giao diện Information
@app.route('/homeLogin')
def homeLogin():
    if "loggedin" in session:
        if session['loggedin'] == True:
            if session['level_loggedin'] == "2":
                return render_template('user.html')
            elif session['level_loggedin'] == "1":
                return render_template('admin.html')
            elif session['level_loggedin'] == "3":
                return render_template('shipper.html')
        else:
            return redirect('/login')
    return redirect('/login')

# Giao diện chính cho User
@app.route('/user')
def user():
    if "user-loggedin" in session:
        if session['user-loggedin'] == True:
            return render_template('user.html')
        else:
            return redirect('/login')
    else:
        return redirect('/login')

# Thông tin đăng nhập
# User
@app.route('/user_information')
def userInformation():
    id = session["user_id"]
    login = Login.find_one({"_id": ObjectId(id)})
    if login is not None:
        return render_template('user/information.html', found_user=login)
    else:
        return 'Login is not found'

# Nạp tiền cho tài khoản User
@app.route('/add_money_user', methods=['GET', 'POST'])
def addMoneyUser():
    user_login = Login.find_one({"_id": ObjectId(session["user_id"])})
    if request.method == 'GET':
        return render_template('user/add-money.html', found_user=user_login)
    elif request.method == 'POST':
        form = request.form
        money = int(form['money'])
        ex_money = int(user_login['balance'])
        balance = money + ex_money

        add_money = {"$set": {
            "balance": balance,
        }}

        Login.update_one(user_login, add_money)
        return redirect('/add_money_user')

# Thêm sản phẩm vào giỏ hàng
@app.route('/add_order/<product_id>', methods=['GET', 'POST'])
def addOrder(product_id):
    if "loggedin" in session:
        if session['loggedin'] == True:
            if session['level_loggedin'] == "2":
                found_user = Login.find_one(
                    {"_id": ObjectId(session["user_id"])})
                found_product = Product.find_one({"_id": ObjectId(product_id)})
                found_order = Order.find_one(
                    {"user_id": session['user_id'], "is_ordered": False, "status": "Shipper chưa nhận đơn"})
                if found_product is not None:
                    if found_order is not None:
                        ex_fee = found_order['order_fee']
                        order_fee = int(found_product['price'])+int(ex_fee)
                        ship_fee = 0.1 * \
                            int(int(found_product['price'])+int(ex_fee))
                        #  Cập nhật giá tiền mới
                        found_order_update_2 = {"$set": {
                            "order_time": datetime.now(),
                            "order_fee": order_fee,
                            "ship_fee": ship_fee,
                            # Thêm 1 sản phẩm vào giỏ hàng
                        }, "$addToSet": {"product_id": {
                            "_id": found_product['_id'],
                            "image": found_product['image'],
                            "name": found_product['name'],
                            "description": found_product['description'],
                            "price": int(found_product['price']),
                            "status": found_product['status'],
                            "brand": found_product['brand'],
                            "product_type": found_product['product_type'],
                            "product_gender": found_product['product_gender'],
                            "product_kids": found_product['product_kids'],
                        }}}
                        Order.update_one(found_order, found_order_update_2)
                        b = session['search']
                        a = "/search/" + b
                        return redirect(a)
                    else:
                        add_order = {
                            "user_id": session['user_id'],
                            "product_id": [{
                                "_id": found_product['_id'],
                                "image": found_product['image'],
                                "name": found_product['name'],
                                "description": found_product['description'],
                                "price": int(found_product['price']),
                                "status": found_product['status'],
                                "brand": found_product['brand'],
                                "product_type": found_product['product_type'],
                                "product_gender": found_product['product_gender'],
                                "product_kids": found_product['product_kids'],
                            }],
                            "address": found_user['address'],
                            "order_time": datetime.now(),
                            "order_fee": int(found_product['price']),
                            "ship_fee": 0.1*int(found_product['price']),
                            "is_ordered": False,
                            "status": "Shipper chưa nhận đơn",
                            "shipper_id": "null",
                        }
                        Order.insert_one(add_order)
                        return redirect('/')
                else:
                    return 'Not found'
            else:
                return redirect('/login')
        else:
            return redirect('/login')
    else:
        return redirect('/login')

# Hiển thị giỏ hàng
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    found_order = Order.find_one(
        {"user_id": session['user_id'], 'is_ordered': False, 'status': "Shipper chưa nhận đơn"})
    if request.method == 'GET':
        if found_order is not None:
            cart = found_order
            order_product = cart['product_id']
            return render_template('user/cart.html', cart=cart, order_product=order_product, template=1)
        else:
            return render_template('user/cart.html', template=0)
    elif request.method == 'POST':
        form = request.form
        request_time = form['request_time']
        update = {"$set": {
            'request_time': request_time,
        }}
        Order.update_one(found_order, update)
    return redirect('/cart')

# Xóa một sản phẩm khỏi giỏ hàng
@app.route('/delete_product/<product_id>')
def delete_product(product_id):
    order = Order.find_one(
        {'user_id': session['user_id'], 'is_ordered': False, 'status': "Shipper chưa nhận đơn"})

    product = Product.find_one({"_id": ObjectId(product_id)})

    Order.update_one(
        {'_id': ObjectId(order['_id'])},
        {'$pull': {"product_id": {'_id': ObjectId(product_id)}}},
    )

    order_fee_ex = int(order['order_fee'])
    product_price = int(product['price'])
    new_order_fee = int(order_fee_ex) - int(product_price)
    new_ship_fee = (0.1 * new_order_fee)
    Order.update_one(
        {'_id': ObjectId(order['_id'])},
        {'$set': {"order_fee": new_order_fee, "ship_fee": new_ship_fee}},
    )
    return redirect('/cart')

# Gửi yêu cầu mua đơn hàng
@app.route('/ordered/<order_id>')
def ordered(order_id):
    found_order = Order.find_one({"_id": ObjectId(order_id)})
    found_user = Login.find_one({"_id": ObjectId(found_order['user_id'])})
    if found_order is not None:
        total = int(found_order['order_fee']) + int(found_order['ship_fee'])
        ex_balance = int(found_user['balance'])
        if ex_balance >= total:
            # Trừ tiền
            balance = ex_balance - total
            update_user = {"$set": {
                "balance": balance,
            }}
            Login.update_one(found_user, update_user)
            #
            update_order = {"$set": {
                "is_ordered": True,
            }}
            Order.update_one(found_order, update_order)
            # Gửi Mail
            gmail = GMail('ngovankhanh108@gmail.com', 'KhanhNgo108')
            html_content = '''Đơn hàng của bạn đã được gửi đi,
                  Tài khoản của bạn sẽ bị trừ đi {{total}}$ tổng chi phí sản phẩm và vận chuyển của đơn hàng này.
                  Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi'''
            html_content1 = html_content.replace("{{total}}", str(total))
            msg = Message(
                'GỬI YÊU CẦU',
                to=found_user['email'],
                html=html_content1
            )
            gmail.send(msg)
            return render_template('user/accepted.html', template=1)
        else:
            return render_template('user/accepted.html', template=0)
    else:
        return 'Order is not found'

# Hiển thị trạng thái đơn hàng đã yêu cầu
@app.route('/order_status')
def orderStatus():
    all_order = Order.find(
        {'user_id': session['user_id'], 'is_ordered': True, 'shipper_id': "null"})
    if all_order is not None:
        return render_template('user/order-status.html', all_order=all_order, template=1)
    else:
        return render_template('user/order-status.html', template=0)

# Hiển thị trạng thái đơn hàng đã yêu cầu và có shipper nhận
@app.route('/order_status_receiver')
def orderStatusReceiver():
    all_order = Order.find({'user_id': session['user_id'], 'is_ordered': True,
                            "status": "Shipper đã nhận hàng, bắt đầu tiến hành vận chuyển"})
    if all_order is not None:
        return render_template('user/order-status.html', all_order=all_order, template=1)
    else:
        return render_template('user/order-status.html', template=0)

# Hai nút tìm kiếm tình trạng các đơn hàng của user
@app.route('/user_status_select')
def user_status_select():
    return render_template('user/user-status-select.html')

# Cập nhật địa chỉ ship đơn hàng
@app.route('/update_address', methods=['GET', 'POST'])
def updateAddress():
    found_order = Order.find_one(
        {'user_id': session['user_id'], 'is_ordered': False, 'status': "Shipper chưa nhận đơn"})
    if request.method == 'GET':
        return render_template('user/update-address.html', found_order=found_order)
    elif request.method == 'POST':
        form = request.form
        address = form['address']
        update = {"$set": {
            "address": address,
        }}
        Order.update_one(found_order, update)
    return redirect('/cart')

# User xác nhận đã nhận được hàng
@app.route('/receive_order/<order_id>')
def receive_order(order_id):
    found_order = Order.find_one({"_id": ObjectId(order_id)})
    if found_order is not None:
            # Chuyển trạng thái đơn
        update1 = {"$set": {
            "status": "User đã nhận hàng",
            "is_ordered": False,
        }}
        Order.update_one(found_order, update1)
        # Add phí vận chuyển cho Shipper
        id_shipper = found_order['shipper_id']
        found_shipper = Login.find_one({"_id": ObjectId(id_shipper)})
        ship_fee = found_order['ship_fee']
        if found_shipper['balance'] == 0:
            update2 = {"$set": {"balance": ship_fee, }}
            Login.update_one(found_shipper, update2)
        else:
            balance = int(found_shipper['balance'])+int(ship_fee)
            update3 = {"$set": {"balance": balance, }}
            Login.update_one(found_shipper, update3)
        # Gửi mail cho Shipper
        gmail = GMail('ngovankhanh108@gmail.com', 'KhanhNgo108')
        html_content = '''Bạn đã vận chuyển thành công đơn hàng đến tay người dùng
                    Bạn sẽ nhận được {{ship_fee}}$ phí ship cho đơn hàng này.
                    Cảm ơn bạn đã tham gia vào hệ thống của chúng tôi'''
        html_content1 = html_content.replace("{{ship_fee}}", str(ship_fee))
        msg = Message(
            'NHẬN ĐƠN',
            to=found_shipper['email'],
            html=html_content1
        )
        gmail.send(msg)
        return redirect('/order_status')
    else:
        return 'Order is not found'

# Hiển thị lịch sử mua hàng
@app.route('/order_history')
def order_history():
    all_order = Order.find(
        {'user_id': session['user_id'], 'is_ordered': False, 'status': "User đã nhận hàng"})
    if all_order is not None:
        return render_template('user/order-history.html', all_order=all_order, template=1)
    else:
        return render_template('user/order-history.html', template=0)

# Todo SHIPPER
# Chức năng của shipper

# Logout shipper login user
@app.route('/logoutShipper_loginUser')
def logoutShipper_loginUser():
    if session['loggedin'] == False:
        return redirect('/login')
    else:
        session['loggedin'] = False
        if session['level_loggedin'] == "1":
            del session['admin_id']
            del session['level_loggedin']
        elif session['level_loggedin'] == "2":
            del session['user_id']
            del session['level_loggedin']
        elif session['level_loggedin'] == "3":
            del session['shipper_id']
            del session['level_loggedin']
        return redirect('/login')

# Đăng ký
@app.route('/sign_up_shipper', methods=['GET', 'POST'])
def signUpShipper():
    if request.method == 'GET':
        return render_template('signup/signup-shipper.html')
    elif request.method == 'POST':
        form = request.form
        fullname = form['fullname']
        username = form['username']
        password = form['password']
        # level = form['level']
        email = form['email']
        phone = form['phone']
        address = form['address']
        id_person = form['id_person']
        # balance = form['balance']

        login = Login.find({"username": username})
        c = int(login.count())
        if c > 0:
            return render_template('signup/signup-fail.html', template=0)
        else:
            new_login = {
                "fullname": fullname,
                "username": username,
                "password": password,
                "level": 3,
                "email": email,
                "phone": phone,
                "id_person": id_person,
                "address": address,
                "balance": 0,
            }
            Login.insert_one(new_login)

            found_login = Login.find_one({'username': username})
            gmail = GMail('ngovankhanh108@gmail.com', 'KhanhNgo108')
            html_content = '''
            Chúc mừng bạn đã tạo tài khoản thành công trên hệ thống.
            Cảm ơn quý khách đã sử dụng dịch vụ của chúng tôi!
            '''
            msg = Message('Tạo tài khoản thành công',
                          to=found_login['email'], html=html_content)
            gmail.send(msg)
            return redirect('/login')

# Thông tin cá nhân
@app.route('/shipper_information')
def shipperInformation():
    login = Login.find_one({"_id": ObjectId(session['shipper_id'])})
    if login is not None:
        return render_template('shipper/information.html', found_shipper=login)
    else:
        return 'Login is not found'

# Cập nhật thông tin cá nhân cho Shipper
@app.route('/shipper_update/<id>', methods=['GET', 'POST'])
def updateShipper(id):
    shipper = Login.find_one({"_id": ObjectId(session['shipper_id'])})
    if shipper is not None:
        if request.method == 'GET':
            return render_template('shipper/shipper-update.html', update_shipper=shipper)
        elif request.method == 'POST':
            form = request.form

            password = form['password']

        update = {"$set": {
            "password": password,
        }}
        Login.update_one(shipper, update)
    else:
        return 'Shipper is not found'
    return redirect('/shipper_information')

# Các đơn hàng hiện có cho shipper
@app.route('/ship_request')
def requestShipper():
    all_order = Order.find(
        {'is_ordered': True, 'status': "Shipper chưa nhận đơn"})
    c = int(all_order.count())
    if c > 0:
        return render_template('shipper/ship-request.html', template=1, all_order=all_order)
    else:
        return render_template('shipper/ship-request.html', template=0)

# Hai nút tìm kiếm tình trạng các đơn Shipper đã nhận
@app.route('/ship_status_select')
def ship_status_select():
    return render_template('shipper/ship-status-select.html')

# Chi tiết đơn hàng
@app.route('/detail_request/<order_id>')
def requestDetail(order_id):
    found_order = Order.find_one({"_id": ObjectId(order_id)})
    if found_order is not None:
        user = Login.find_one({"_id": ObjectId(found_order['user_id'])})
        order_product = found_order['product_id']
        return render_template('shipper/detail-request.html', found_order=found_order, user=user, order_product=order_product)
    else:
        return 'Order is not found'

# Lịch sử ship đơn hàng
@app.route('/shipped_history')
def historyShipper():
    all_order = Order.find(
        {'shipper_id': session['shipper_id'], 'status': "User đã nhận hàng"})
    c = int(all_order.count())
    if c > 0:
        return render_template('shipper/shipped-history.html', all_order=all_order, template=1)
    else:
        return render_template('shipper/shipped-history.html', template=0)

# Shipper nhận đơn hàng
@app.route('/shipper_accepted_order/<order_id>')
def shipper_accepted_order(order_id):
    found_order = Order.find_one({"_id": ObjectId(order_id)})
    if found_order is not None:
        id_user = found_order['user_id']
        found_user = Login.find_one({"_id": ObjectId(id_user)})
        # Thêm ID của Shipper vào đơn và #Đổi trạng thái đơn
        update = {"$set": {"shipper_id": session['shipper_id'],
                           "status": "Shipper đã nhận đơn, đang tiến hành lấy hàng"}}
        Order.update_one(found_order, update)
        # Gửi Mail cho User
        gmail = GMail('ngovankhanh108@gmail.com', 'KhanhNgo108')
        html_content = '''Đơn hàng của bạn đã được Shipper chấp nhận giao hàng, vui lòng kiểm tra tình trạng đơn.
                Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi'''
        msg = Message(
            'NHẬN ĐƠN',
            to=found_user['email'],
            html=html_content
        )
        gmail.send(msg)
        return redirect('/ship_request')
    else:
        return 'Order is not found'

# Xem thông tin đơn hiện tại Shipper chấp nhận vận chuyển
@app.route('/ship_status/<status>')
def ship_status(status):
    found_order = Order.find(
        {'shipper_id': session['shipper_id'], 'status': status})
    c = int(found_order.count())
    if c > 0:
        return render_template('shipper/ship-status.html', found_order=found_order, template=1)
    else:
        return render_template('shipper/ship-status.html', template=0)

# Shipper xác nhận đã lấy hàng
@app.route('/product_request/<order_id>')
def product_request(order_id):
    found_order = Order.find_one({"_id": ObjectId(order_id)})
    if found_order is not None:
        id_user = found_order['user_id']
        found_user = Login.find_one({"_id": ObjectId(id_user)})
        update = {
            "$set": {"status": "Shipper đã nhận hàng, bắt đầu tiến hành vận chuyển"}}
        Order.update_one(found_order, update)
        gmail = GMail('ngovankhanh108@gmail.com', 'KhanhNgo108')
        msg = Message(
            'LẤY HÀNG', to=found_user['email'], html="Shipper đã lấy được hàng, bắt đầu vận chuyển đến bạn")
        gmail.send(msg)
        return redirect('/shipped_history')
    else:
        return 'Order is not found'


# TODO Admin
# Chức năng của admin
# Information Admin
@app.route('/admin_information')
def adminInformation():
    login = Login.find_one({"_id": ObjectId(session["admin_id"])})
    if login is not None:
        return render_template('admin/information.html', found_admin=login)
    else:
        return 'Login is not found'

# Update thông tin admin
@app.route('/admin_update/<id>', methods=['GET', 'POST'])
def updateInfoAdmin(id):
    login = Login.find_one({"_id": ObjectId(id)})
    if request.method == 'GET':
        return render_template('admin/admin-update.html', update_admin=login)
    elif request.method == 'POST':
        form = request.form

        password = form['password']

        update_login = {"$set": {
            "password": password,
        }}
        Login.update_one(login, update_login)
        return redirect('/homeLogin')

# Hiển thị sản phẩm
@app.route('/all_product_admin')
def allProduct():
    all_product = Product.find()
    return render_template('admin/all_product.html', all_product=all_product)

# Xóa sản phẩm
@app.route('/product/delete/<id>')
def deleteProduct(id):
    product = Product.find_one({"_id": ObjectId(id)})
    Product.delete_one(product)
    return redirect('/all_product')

# Sửa sản phẩm
@app.route('/all_product/update_product/<id>', methods=['GET', 'POST'])
def updateProduct(id):
    product = Product.find_one({"_id": ObjectId(id)})
    if request.method == 'GET':
        return render_template('update_product.html', product=product)
    elif request.method == 'POST':
        form = request.form

        image = form['image']
        name = form['name']
        description = form['description']
        status = form['status']
        price = form['price']
        brand = form['brand']
        product_type = form['product_type']
        product_gender = form['product_gender']
        product_kids = form['product_kids']

        update_product = {"$set": {
            "image": image,
            "name": name,
            "description": description,
            "price": price,
            "status": status,
            "brand": brand,
            "product_type": product_type,
            "product_gender": product_gender,
            "product_kids": product_kids,
        }}
        Product.update_one(product, update_product)
        return redirect('/all_product')

# Thêm sản phẩm
@app.route('/add_product', methods=['GET', 'POST'])
def addProduct():
    if request.method == 'GET':
        return render_template('add_product.html')
    elif request.method == 'POST':
        form = request.form

        image = form['image']
        name = form['name']
        description = form['description']
        status = form['status']
        price = form['price']
        brand = form['brand']
        product_type = form['product_type']
        product_gender = form['product_gender']
        product_kids = form['product_kids']

        new_product = {
            "image": image,
            "name": name,
            "description": description,
            "status": status,
            "price": price,
            "brand": brand,
            "product_type": product_type,
            "product_gender": product_gender,
            "product_kids": product_kids,
        }

        Product.insert_one(new_product)
        return redirect('/all_product')

# Quản lý tài khoản
@app.route('/all_login')
def allLogin():
    all_login = Login.find()
    # Tổng số bản ghi
    count_all_login = Login.count()
    # Số bản ghi max trên 1 trang
    maxA = 2
    # Tổng số trang
    all_page = count_all_login / maxA
    # Trang hiện thời
    current_page = 1
    # Start
    start = (current_page - 1) * maxA
    return render_template('admin/all_login.html', all_login=all_login, count_all_login=count_all_login, maxA=maxA, all_page=all_page, current_page=current_page, start=start)

# Xóa tài khoản
@app.route('/all_login/delete/<id>')
def deleteLogin(id):
    login = Login.find_one({"_id": ObjectId(id)})
    Login.delete_one(login)
    return redirect('/all_login')

# Xuất file Excel Account
@app.route('/output_excel')
def output_excel():
    all_login = Login.find()
    data = []
    i = 0
    for login in all_login:
        list_login = {}
        #
        index = i
        fullname = login['fullname']
        username = login['username']
        password = login['password']
        level = login['level']
        email = login['email']
        phone = login['phone']
        balance = login['balance']
        #
        list_login['STT'] = index
        list_login['Fullname'] = fullname
        list_login['Username'] = username
        list_login['Password'] = password
        list_login['Level'] = level
        list_login['Email'] = email
        list_login['Phone'] = phone
        list_login['Balance'] = balance
        i = i + 1
        #
        data.append(list_login)
    pyexcel.save_as(records=data, dest_file_name="TestLogins.xlsx")
    return "Done"


if __name__ == '__main__':
    app.run(debug=True)
