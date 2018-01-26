from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL

class newCategoryForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(max=64)])
    description = TextAreaField('Description',
                                validators=[DataRequired(), Length(max=250)])
    submit = SubmitField('CREATE')


class editCategoryForm(FlaskForm):
    id = IntegerField(validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    description = TextAreaField('Description',
                                validators=[DataRequired(), Length(max=250)])
    submit = SubmitField('EDIT')


class deleteCategoryForm(FlaskForm):
    id = IntegerField(validators=[DataRequired()])
    submit = SubmitField('CONFIRM')


class newItemForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(max=64)])
    description = TextAreaField('Description',
                                validators=[DataRequired(), Length(max=250)])
    picture = StringField('Picture URL',
                            validators=[Optional(), URL()])
    submit = SubmitField('CREATE')


class editItemForm(FlaskForm):
    id = IntegerField(validators=[DataRequired()])
    name = StringField('Name',
                        validators=[DataRequired(), Length(max=64)])
    description = TextAreaField('Description',
                                validators=[DataRequired(), Length(max=250)])
    picture = StringField('Picture URL',
                            validators=[Optional(), URL()])
    submit = SubmitField('EDIT')


class deleteItemForm(FlaskForm):
    id = IntegerField(validators=[DataRequired()])
    submit = SubmitField('CONFIRM')
