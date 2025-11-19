from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homepaint.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------------
# MODELS
# -------------------------
class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))


class Painter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    experience = db.Column(db.String(50))
    speciality = db.Column(db.String(100))
    city = db.Column(db.String(100))
    password = db.Column(db.String(50))   # 🔥 ADDED
    is_active = db.Column(db.Boolean, default=True)



class ClientBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    area_type = db.Column(db.String(50))
    room_size = db.Column(db.String(50))
    number_of_rooms = db.Column(db.String(20))
    surface_type = db.Column(db.String(50))
    wall_condition = db.Column(db.String(100))
    paint_type = db.Column(db.String(100))
    paint_brand = db.Column(db.String(50))
    paint_coats = db.Column(db.String(50))
    furniture_shift = db.Column(db.String(50))
    ceiling_paint = db.Column(db.String(50))
    paint_removal = db.Column(db.String(50))
    budget = db.Column(db.String(50))
    notes = db.Column(db.String(300))
    work_date = db.Column(db.String(50))
    service_type = db.Column(db.String(50))
    rate = db.Column(db.String(50))
    status = db.Column(db.String(50), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.now)

    painter_id = db.Column(db.Integer, db.ForeignKey('painter.id'))
    painter = db.relationship('Painter', backref='bookings')


# -------------------------
# LOGIN REQUIRED DECORATOR
# -------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please login first!", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/painter/login', methods=['GET', 'POST'])
def painter_login():
    if request.method == 'POST':
        painter = Painter.query.filter_by(
            phone=request.form['phone'],
            password=request.form['password']
        ).first()

        if painter:
            session['painter_id'] = painter.id
            flash("Login successful!", "success")
            return redirect(url_for('painter_dashboard'))

        flash("Invalid credentials!", "danger")

    return render_template('painter_login.html')

@app.route('/painter/dashboard')
def painter_dashboard():
    if "painter_id" not in session:
        return redirect(url_for('painter_login'))

    bookings = ClientBooking.query.filter_by(painter_id=session['painter_id']).all()
    return render_template('painter_dashboard.html', bookings=bookings)

@app.route('/painter/update/<int:id>', methods=['POST'])
def painter_update_status(id):
    if "painter_id" not in session:
        return redirect(url_for('painter_login'))

    booking = ClientBooking.query.get_or_404(id)

    if booking.painter_id != session['painter_id']:
        flash("Unauthorized!", "danger")
        return redirect(url_for('painter_dashboard'))

    booking.status = request.form.get('status')
    db.session.commit()

    flash("Status updated!", "success")
    return redirect(url_for('painter_dashboard'))



# -------------------------
# CLIENT ROUTES
# -------------------------
@app.route('/')
def home():
    return render_template('client_booking.html')


@app.route('/book', methods=['POST'])
def book_service():
    booking = ClientBooking(
        name=request.form.get('name'),
        phone=request.form.get('phone'),
        address=request.form.get('address'),
        area_type=request.form.get('area_type'),
        room_size=request.form.get('room_size'),
        number_of_rooms=request.form.get('number_of_rooms'),
        surface_type=request.form.get('surface_type'),
        wall_condition=request.form.get('wall_condition'),
        paint_type=request.form.get('paint_type'),
        paint_brand=request.form.get('paint_brand'),
        paint_coats=request.form.get('paint_coats'),
        furniture_shift=request.form.get('furniture_shift'),
        ceiling_paint=request.form.get('ceiling_paint'),
        paint_removal=request.form.get('paint_removal'),
        budget=request.form.get('budget'),
        notes=request.form.get('notes'),
        work_date=request.form.get('work_date'),
        service_type=request.form.get('service_type'),
        painter_id=None
    )

    db.session.add(booking)
    db.session.commit()

    flash("🎉 Your booking has been submitted! We will contact you soon.", "success")
    return redirect(url_for('home'))


# -------------------------
# ADMIN AUTH
# -------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = AdminUser.query.filter_by(
            username=request.form['username'],
            password=request.form['password']
        ).first()

        if user:
            session['user'] = user.username
            flash("Welcome!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password", "danger")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))


# -------------------------
# DASHBOARD
# -------------------------
@app.route('/dashboard')
@login_required
def dashboard():
    bookings = ClientBooking.query.order_by(ClientBooking.created_at.desc()).all()
    return render_template('index.html', bookings=bookings)


# -------------------------
# ASSIGN PAINTER
# -------------------------
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_booking(id):
    booking = ClientBooking.query.get_or_404(id)

    if request.method == 'POST':
        booking.rate = request.form.get('rate')
        booking.status = request.form.get('status')
        booking.painter_id = request.form.get('painter_id')

        db.session.commit()
        flash("Booking updated successfully!", "info")
        return redirect(url_for('dashboard'))

    painters = Painter.query.filter_by(is_active=True).all()
    return render_template('view_booking.html', booking=booking, painters=painters)


@app.route('/delete/<int:id>')
@login_required
def delete_booking(id):
    booking = ClientBooking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    flash("Booking deleted!", "danger")
    return redirect(url_for('dashboard'))


# -------------------------
# PAINTER MANAGEMENT
# -------------------------
@app.route('/painters')
@login_required
def painters_list():
    painters = Painter.query.all()
    return render_template('painters.html', painters=painters)


@app.route('/painters/add', methods=['GET', 'POST'])
@login_required
def add_painter():
    if request.method == 'POST':
        painter = Painter(
            name=request.form.get('name'),
            phone=request.form.get('phone'),
            experience=request.form.get('experience'),
            speciality=request.form.get('speciality'),
            city=request.form.get('city'),
            password=request.form.get('password'),  # 🔥 ADDED
            is_active=True
        )
        db.session.add(painter)
        db.session.commit()
        flash("Painter added successfully!", "success")
        return redirect(url_for('painters_list'))

    return render_template('add_painter.html')


@app.route('/painters/toggle/<int:id>')
@login_required
def toggle_painter(id):
    painter = Painter.query.get_or_404(id)
    painter.is_active = not painter.is_active
    db.session.commit()
    flash("Painter status updated!", "info")
    return redirect(url_for('painters_list'))


# -------------------------
# INITIAL SETUP
# -------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        if not AdminUser.query.filter_by(username="admin").first():
            db.session.add(AdminUser(username="admin", password="1234"))
            db.session.commit()

    app.run(debug=True)
