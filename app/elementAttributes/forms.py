from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import DateTimeField, FloatField, HiddenField, SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required
from .. models import Area, ElementAttributeTemplate, Element, ElementTemplate, Enterprise, Site, Tag
from .. helpers import elementAttributeTemplateFullyAbbreviatedPath, elementFullyAbbreviatedPath, tagFullyAbbreviatedPath

class ElementAttributeForm(FlaskForm):
	element = QuerySelectField(query_factory = lambda: Element.query.join(ElementTemplate, Site, Enterprise). \
		order_by(Enterprise.Abbreviation, Site.Abbreviation, ElementTemplate.Name, Element.Name), get_label = elementFullyAbbreviatedPath)
	elementAttributeTemplate = QuerySelectField("Element Attribute Template", query_factory = lambda: ElementAttributeTemplate.query.join(ElementTemplate, Site, Enterprise). order_by(Enterprise.Abbreviation, Site.Abbreviation, ElementTemplate.Name, ElementAttributeTemplate.Name), \
		get_label = elementAttributeTemplateFullyAbbreviatedPath)
	tag = QuerySelectField(query_factory = lambda: Tag.query.join(Area, Site, Enterprise). \
		order_by(Enterprise.Abbreviation, Site.Abbreviation, Area.Abbreviation, Tag.Name), get_label = tagFullyAbbreviatedPath)
	submit = SubmitField("Save")

class ElementAttributeImportForm(FlaskForm):
	elementAttributesFile = FileField("Element Attributes Import File", validators = [FileRequired(), FileAllowed(["csv"], ".csv files only!")])
	submit = SubmitField("Import")

class ElementAttributeValueForm(FlaskForm):
	tagId = HiddenField()
	timestamp = DateTimeField("Timestamp", default = datetime.now, validators = [Required()])
	value = FloatField("Value")
	lookupValue = SelectField("Lookup", coerce = float)
	submit = SubmitField("Save")
