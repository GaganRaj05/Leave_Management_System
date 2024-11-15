from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField, TextAreaField, DateField,IntegerField,SelectField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username",validators= [DataRequired(), Length(min = 3, max =20)])
    password = PasswordField("Password", validators= [DataRequired(), Length(min = 4, max=20)])
    confirm = SubmitField("Login")
    
class WriteALeave(FlaskForm):
    roll_no = StringField("Enter your Register number ", validators=[DataRequired(),Length(max = 10)])
    by = StringField("Enter your name",validators=[DataRequired(),Length(min=4)])
    to = StringField("Enter the User Id of the receiver", validators=[DataRequired(), Length(min=3)])
    dFrom = DateField("Data From",validators=[DataRequired()])
    dTo = DateField("Data To",validators=[DataRequired()])
    subject = StringField("Subject",  validators=[DataRequired(),Length(min=4)])
    bodyL = TextAreaField("Reason",validators=[DataRequired(),Length(min=10)])
    cancel = SubmitField('Cancel')
    submit = SubmitField("Submit")
    
class viewLetter(FlaskForm):
    decline = SubmitField('Decline')
    approve = SubmitField('Approve')
    
class editStudent(FlaskForm):
    Name = StringField('Student Name',validators=[DataRequired()])
    RegNo = StringField('Register-No', validators=[DataRequired()])
    Branch = SelectField("Branch name", validators=[DataRequired()], choices=[('CS', 'CS'), ('EC', 'EC'), ('MECH', 'MECH'), ('CIVIL', 'CIVIL')])
    Password = StringField("Password",validators=[DataRequired()])
    cancel = SubmitField("Cancel")
    submit = SubmitField("Edit")
    
class editstaff(FlaskForm):
    Name = StringField('Staff Name',validators=[DataRequired()])
    StaffId = StringField('Staff-No', validators=[DataRequired()])
    Branch = SelectField("Branch name", validators=[DataRequired()], choices=[('CS', 'CS'), ('EC', 'EC'), ('MECH', 'MECH'), ('CIVIL', 'CIVIL')])
    Password = StringField("Password",validators=[DataRequired()])
    cancel = SubmitField("Cancel")
    submit = SubmitField("Edit")
    
class AddStudent(FlaskForm):
    Name=StringField("Student Name",validators=[DataRequired()])
    RegNo = StringField('Register-No', validators=[DataRequired()])
    Branch = SelectField("Branch name", validators=[DataRequired()], choices=[('CS', 'CS'), ('EC', 'EC'), ('MECH', 'MECH'), ('CIVIL', 'CIVIL')])
    Password = StringField("Password",validators=[DataRequired()])
    cancel = SubmitField("Cancel")
    submit = SubmitField("Add")
    
class AddStaff(FlaskForm):
    Name = StringField('Staff Name',validators=[DataRequired()])
    StaffId = StringField('Staff-No', validators=[DataRequired()])
    Branch = SelectField("Branch name", validators=[DataRequired()], choices=[('CS', 'CS'), ('EC', 'EC'), ('MECH', 'MECH'), ('CIVIL', 'CIVIL')])

    Password = StringField("Password",validators=[DataRequired()])
    cancel = SubmitField("Cancel")
    submit = SubmitField("Add")