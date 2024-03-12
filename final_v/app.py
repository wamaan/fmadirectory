from flask import Flask, render_template, redirect, flash, url_for,Response,request
from flask_login import login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap5
from extensions import db, bcrypt, login_manager
from models import User, Member
from forms import RegistrationForm, LoginForm, MemberForm
import os
import csv
from io import StringIO
import pandas as pd

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please login first"
login_manager.login_message_category = "danger"

Bootstrap5(app)

# User authentication and authorization
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.before_first_request
def create_table():
    db.create_all()
    print('database table created')


@app.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successfully.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "error")
    return render_template("form.html", form=form, title="Login")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, role="user")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))
    return render_template("form.html", form=form, title="Register")


@app.route("/dashboard")
@login_required
def dashboard():
    members = Member.query.all()
    return render_template("dashboard.html", members=members)


@app.route("/create_member", methods=["GET", "POST"])
@login_required
def create_member():
    form = MemberForm()
    if form.validate_on_submit():
        new_member = Member(
            banner_id=form.banner_id.data,
            tiger_email=form.tiger_email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            personal_email=form.personal_email.data,
            current_city=form.current_city.data,
            current_employer=form.current_employer.data,
            graduation_date=form.graduation_date.data,
            linkedin=form.linkedin.data,
            graduating_employer=form.graduating_employer.data,
            internship1=form.internship1.data,
            internship2=form.internship2.data,
            internship3=form.internship3.data,
            additional_degrees=form.additional_degrees.data,
            address=form.address.data
        )
        db.session.add(new_member)
        db.session.commit()
        flash('Member added successfully', 'success')
        return redirect(url_for("dashboard"))
    return render_template("form.html", form=form, title="Create Member")


@app.route("/edit_member/<int:member_id>", methods=["GET", "POST"])
@login_required
def edit_member(member_id):
    member = Member.query.get_or_404(member_id)
    form = MemberForm(obj=member)
    if form.validate_on_submit():
        member.banner_id=form.banner_id.data
        member.tiger_email=form.tiger_email.data
        member.first_name=form.first_name.data
        member.last_name=form.last_name.data
        member.phone=form.phone.data
        member.personal_email=form.personal_email.data
        member.current_city=form.current_city.data
        member.current_employer=form.current_employer.data
        member.graduation_date=form.graduation_date.data
        member.linkedin=form.linkedin.data
        member.graduating_employer=form.graduating_employer.data
        member.internship1=form.internship1.data
        member.internship2=form.internship2.data
        member.internship3=form.internship3.data
        member.additional_degrees=form.additional_degrees.data
        member.address=form.address.data

        db.session.commit()
        flash("Member updated successfully.", "success")
        return redirect(url_for("dashboard"))
    return render_template("form.html", form=form, title="Update Member")



@app.route("/delete_member/<int:member_id>", methods=["POST"])
@login_required
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    if member:
        db.session.delete(member)
        db.session.commit()
        flash("Member deleted successfully.", "success")
    return redirect(url_for("dashboard"))



@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout successfully.", "success")
    return redirect(url_for("login"))

@app.route('/export_csv')
@login_required
def export_csv():

    
    members = Member.query.all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["BannerID", "Tigermail", "First_Name", "Last_Name", "Phone", "Email",
                     "Current City", "Current_Employer", "Graduation_Date", "Linkedin", "Graduating_Employer",
                     "Internship_Junior", "Internship_Sophomore", "Internship_Freshman", "Additional_Degrees", "Address"])

    for member in members:
        writer.writerow([member.banner_id, member.tiger_email, member.first_name, member.last_name, member.phone,
                         member.personal_email, member.current_city, member.current_employer, member.graduation_date,
                         member.linkedin, member.graduating_employer, member.internship1, member.internship2,
                         member.internship3, member.additional_degrees, member.address])

    output.seek(0)

    response = Response(output.getvalue(), content_type='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename=members.csv"

    return response


@app.route('/upload_csv', methods=['POST'])
@login_required
def upload_csv():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect('dashboard')

        file = request.files['file']

        # Check if the file is not empty
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect('dashboard')

        # Check if the file has a valid extension
        if file and file.filename.rsplit('.', 1)[1].lower() == 'csv':
            try:
                df = pd.read_csv(file)

                # Map CSV column names to model attribute names
                column_mapping = {
                    "BannerID": "banner_id",
                    "Tigermail": "tiger_email",
                    "First_Name": "first_name",
                    "Last_Name": "last_name",
                    "Phone": "phone",
                    "Email": "personal_email",
                    "Current City": "current_city",
                    "Current_Employer": "current_employer",
                    "Graduation_Date": "graduation_date",
                    "Linkedin": "linkedin",
                    "Graduating_Employer": "graduating_employer",
                    "Internship_Junior": "internship1",
                    "Internship_Sophomore": "internship2",
                    "Internship_Freshman": "internship3",
                    "Additional_Degrees": "additional_degrees",
                    "Address": "address"
                }

                # Rename columns in the DataFrame
                df.rename(columns=column_mapping, inplace=True)
                
                if df.empty:
                    flash('No valid data found in the CSV file. Please check if data is present or if the date format is correct.', 'danger')
                    return redirect('dashboard')
                
                # Add data to the members table
                df.to_sql('member', db.engine, if_exists='append', index=False)

                flash('File uploaded and data added successfully', 'success')
                return redirect(url_for('dashboard'))

            except Exception as e:
                print(e)
                flash(f'Error processing CSV file: {str(e)}', 'error')
                return redirect(url_for('dashboard'))
        else:
            flash('Upload csv file only', 'danger')
            return redirect(url_for('dashboard'))




if __name__ == "__main__":
    app.run(debug=True)
