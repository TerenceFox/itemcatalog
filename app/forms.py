from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class newCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=64)])
    description = TextAreaField('Category Description',
                                validators=[DataRequired(), Length(max=250)])
    submit = SubmitField('CREATE')


class editCategoryForm(FlaskForm):
    id = IntegerField(validators=[DataRequired()])
    name = StringField('Category Name', validators=[DataRequired(), Length(max=64)])
    description = TextAreaField('Category Description',
                                validators=[DataRequired(), Length(max=250)])
    submit = SubmitField('EDIT')

class deleteCategoryForm(FlaskForm):
    id = IntegerField(validators=[DataRequired()])
    submit = SubmitField('CONFIRM')
