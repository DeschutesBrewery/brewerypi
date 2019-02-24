from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from . import eventFrameAttributeTemplates
from . forms import EventFrameAttributeTemplateForm
from .. import db
from .. decorators import adminRequired
from .. models import Area, EventFrameAttribute, EventFrameAttributeTemplate, EventFrameTemplate, Lookup, LookupValue, Tag

@eventFrameAttributeTemplates.route("/eventFrameAttributeTemplates/add/eventFrameTemplateId/<int:eventFrameTemplateId>", methods = ["GET", "POST"])
@eventFrameAttributeTemplates.route("/eventFrameAttributeTemplates/add/eventFrameTemplateId/<int:eventFrameTemplateId>/<int:lookup>", methods = ["GET", "POST"])
@login_required
@adminRequired
def addEventFrameAttributeTemplate(eventFrameTemplateId, lookup = False):
	operation = "Add"
	form = EventFrameAttributeTemplateForm()
	eventFrameTemplate = EventFrameTemplate.query.get_or_404(eventFrameTemplateId)
	if lookup:
		modelName = "Lookup Event Frame Attribute Template"
		del form.defaultEndValue
		del form.defaultStartValue
		del form.unitOfMeasurement
		lookupQuery = Lookup.query.filter_by(EnterpriseId = eventFrameTemplate.origin().ElementTemplate.Site.Enterprise.EnterpriseId).order_by(Lookup.Name)
		form.lookup.query = lookupQuery
		firstLookup = lookupQuery.first()
		choices = []
		choices.append((-1, ""))
		for lookupValue in LookupValue.query.filter_by(LookupId = firstLookup.LookupId).order_by(LookupValue.Name):
			choices.append((lookupValue.Value, lookupValue.Name))

		form.defaultEndLookupValue.choices = choices
		form.defaultStartLookupValue.choices = choices
	else:
		modelName = "Event Frame Attribute Template"
		del form.defaultStartLookupValue
		del form.defaultEndLookupValue
		del form.lookup

	# Add a new eventFrameAttributeTemplate
	if form.validate_on_submit():
		if lookup:
			defaultEndValue = None if form.defaultEndLookupValue.data == -1 else form.defaultEndLookupValue.data
			defaultStartValue = None if form.defaultStartLookupValue.data == -1 else form.defaultStartLookupValue.data
			eventFrameAttributeTemplate = EventFrameAttributeTemplate(DefaultEndValue = defaultEndValue, DefaultStartValue = defaultStartValue,
				Description = form.description.data, EventFrameTemplateId = eventFrameTemplateId, Lookup = form.lookup.data, Name = form.name.data)
		else:
			defaultEndValue = None if form.defaultEndValue.data is None else form.defaultEndValue.data,
			defaultStartValue = None if form.defaultStartValue.data is None else form.defaultStartValue.data,
			eventFrameAttributeTemplate = EventFrameAttributeTemplate(DefaultEndValue = defaultEndValue, DefaultStartValue = defaultStartValue,
				Description = form.description.data, EventFrameTemplateId = eventFrameTemplateId, Name = form.name.data,
				UnitOfMeasurement = form.unitOfMeasurement.data)

		db.session.add(eventFrameAttributeTemplate)
		db.session.commit()
		flash('You have successfully added the new event frame attribute template "{}" to the event frame template "{}".'. \
			format(eventFrameAttributeTemplate.Name, eventFrameAttributeTemplate.EventFrameTemplate.Name), "alert alert-success")
		createdTags = []
		updatedTags = []
		createdEventFrameAttributes = []
		for element in eventFrameTemplate.ElementTemplate.Elements:
			if element.isManaged():
				# Tag management.
				area = Area.query.get_or_404(element.TagAreaId)
				tagName = "{}_{}".format(element.Name, eventFrameAttributeTemplate.Name.replace(" ", ""))
				tag = Tag.query.filter_by(AreaId = area.AreaId, Name = tagName).one_or_none()
				if tag is None:
					# Tag doesn't exist, so create it.
					tag = Tag(AreaId = area.AreaId, LookupId = eventFrameAttributeTemplate.LookupId, Name = tagName,
						UnitOfMeasurementId = eventFrameAttributeTemplate.UnitOfMeasurementId)
					db.session.add(tag)
					createdTags.append(tag)
				else:
					# Tag exists, so update LookupId and UnitOfMeasurementId just in case.
					tag.LookupId = eventFrameAttributeTemplate.LookupId
					tag.UnitOfMeasurementId = eventFrameAttributeTemplate.UnitOfMeasurementId
					updatedTags.append(tag)

				db.session.commit()

				# Event Frame attribute management.
				eventFrameAttribute = EventFrameAttribute(ElementId = element.ElementId,
					EventFrameAttributeTemplateId = eventFrameAttributeTemplate.EventFrameAttributeTemplateId, TagId = tag.TagId)
				db.session.add(eventFrameAttribute)
				db.session.commit()
				createdEventFrameAttributes.append(eventFrameAttribute)

		createdTagsMessage = ""
		if createdTags:
			createdTags.sort(key = lambda tag: tag.Name)
			for tag in createdTags:
				if createdTagsMessage == "":
					createdTagsMessage = 'Created the following tag(s):<br>"{}"'.format(tag.Name)
					alert = "alert alert-success"
				else:
					createdTagsMessage = '{}<br>"{}"'.format(createdTagsMessage, tag.Name)

			flash(createdTagsMessage, alert)

		updatedTagsMessage = ""
		if updatedTags:
			updatedTags.sort(key = lambda tag: tag.Name)
			for tag in updatedTags:
				if updatedTagsMessage == "":
					updatedTagsMessage = 'Updated the following existing tag(s), if needed:<br>"{}"'.format(tag.Name)
					alert = "alert alert-warning"
				else:
					updatedTagsMessage = '{}<br>"{}"'.format(updatedTagsMessage, tag.Name)

			flash(updatedTagsMessage, alert)

		createdEventFrameAttributesMessage = ""
		if createdEventFrameAttributes:
			createdEventFrameAttributes.sort(key = lambda tag: tag.Element.Name)
			for eventFrameAttribute in createdEventFrameAttributes:
				if createdEventFrameAttributesMessage == "":
					createdEventFrameAttributesMessage = "Created the following event frame attribute(s):<br>Element: " + \
						'{}" attribute: "{}" associated with tag: "{}"'.format(eventFrameAttribute.Element.Name, eventFrameAttribute.EventFrameAttributeTemplate.Name,
						eventFrameAttribute.Tag.Name)
					alert = "alert alert-success"
				else:
					createdEventFrameAttributesMessage = '{}<br>Element: "{}" attribute: "{}" associated with tag: "{}"'.format(createdEventFrameAttributesMessage,
						eventFrameAttribute.Element.Name, eventFrameAttribute.EventFrameAttributeTemplate.Name, eventFrameAttribute.Tag.Name)

			flash(createdEventFrameAttributesMessage, alert)

		return redirect(form.requestReferrer.data)

	# Present a form to add a new event frame attribute template.
	form.eventFrameTemplateId.data = eventFrameTemplateId
	if form.requestReferrer.data is None:
		form.requestReferrer.data = request.referrer

	if eventFrameTemplate.hasParent():
		breadcrumbs = [{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "Root"), "text" : "<span class = \"glyphicon glyphicon-home\"></span>"},
			{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "Enterprise",
				selectedId = eventFrameTemplate.origin().ElementTemplate.Site.Enterprise.EnterpriseId),
				"text" : eventFrameTemplate.origin().ElementTemplate.Site.Enterprise.Name},
			{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "Site",
				selectedId = eventFrameTemplate.origin().ElementTemplate.Site.SiteId), "text" : eventFrameTemplate.origin().ElementTemplate.Site.Name},
			{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "ElementTemplate",
				selectedId = eventFrameTemplate.origin().ElementTemplate.ElementTemplateId), "text" : eventFrameTemplate.origin().ElementTemplate.Name}]
		for eventFrameTemplateAcestor in eventFrameTemplate.ancestors([]):
			breadcrumbs.append({"url" : url_for("eventFrames.selectEventFrame", selectedClass = "EventFrame",
				selectedId = eventFrameTemplateAcestor.EventFrameTemplateId), "text" : eventFrameTemplateAcestor.Name})

		breadcrumbs.append({"url" : url_for("eventFrames.selectEventFrame", selectedClass = "EventFrame",
			selectedId = eventFrameTemplate.EventFrameTemplateId),
			"text" : eventFrameTemplate.Name})
	else:
		breadcrumbs = [{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "Root"), "text" : "<span class = \"glyphicon glyphicon-home\"></span>"},
			{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "Enterprise",
				selectedId = eventFrameTemplate.ElementTemplate.Site.Enterprise.EnterpriseId),
				"text" : eventFrameTemplate.ElementTemplate.Site.Enterprise.Name},
			{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "Site",
				selectedId = eventFrameTemplate.ElementTemplate.Site.SiteId),
				"text" : eventFrameTemplate.ElementTemplate.Site.Name},
			{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "ElementTemplate",
				selectedId = eventFrameTemplate.ElementTemplate.ElementTemplateId), "text" : eventFrameTemplate.ElementTemplate.Name},
			{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "EventFrameTemplate",
				selectedId = eventFrameTemplate.EventFrameTemplateId, selectedOperation = "configure"),
				"text" : eventFrameTemplate.Name}]

	return render_template("eventFrameAttributeTemplates/addEdit.html", breadcrumbs = breadcrumbs, form = form, modelName = modelName, operation = operation)

@eventFrameAttributeTemplates.route("/eventFrameAttributeTemplates/delete/eventFrameAttributeTemplateId/<int:eventFrameAttributeTemplateId>",
	methods = ["GET", "POST"])
@login_required
@adminRequired
def deleteEventFrameAttributeTemplate(eventFrameAttributeTemplateId):
	eventFrameAttributeTemplate = EventFrameAttributeTemplate.query.get_or_404(eventFrameAttributeTemplateId)
	tags = []
	for eventFrameAttribute in eventFrameAttributeTemplate.EventFrameAttributes:
		if eventFrameAttribute.Element.isManaged():
			tags.append(eventFrameAttribute.Tag)

	eventFrameAttributeTemplate.delete()
	db.session.commit()
	flash("You have successfully deleted the event frame attribute template \"{}\".".format(eventFrameAttributeTemplate.Name), "alert alert-success")
	deletedTagsMessage = ""
	tags.sort(key = lambda tag: tag.Name)
	for tag in tags:
		if not tag.isReferenced():
			tag.delete()
			if deletedTagsMessage == "":
				deletedTagsMessage = 'Deleted the following tag(s):<br>"{}"'.format(tag.Name)
			else:
				deletedTagsMessage = '{}<br>"{}"'.format(deletedTagsMessage, tag.Name)

	db.session.commit()
	if deletedTagsMessage != "":
		alert = "alert alert-success"
		flash(deletedTagsMessage, alert)
	return redirect(request.referrer)

@eventFrameAttributeTemplates.route("/eventFrameAttributeTemplates/edit/eventFrameAttributeTemplateId/<int:eventFrameAttributeTemplateId>",
	methods = ["GET", "POST"])
@login_required
@adminRequired
def editEventFrameAttributeTemplate(eventFrameAttributeTemplateId):
	operation = "Edit"
	eventFrameAttributeTemplate = EventFrameAttributeTemplate.query.get_or_404(eventFrameAttributeTemplateId)
	eventFrameTemplateId = eventFrameAttributeTemplate.EventFrameTemplate.EventFrameTemplateId
	form = EventFrameAttributeTemplateForm(obj = eventFrameAttributeTemplate)

	if eventFrameAttributeTemplate.LookupId:
		modelName = "Lookup Event Frame Attribute Template"
		del form.defaultEndValue
		del form.defaultStartValue
		del form.unitOfMeasurement
		lookupQuery = Lookup.query.filter_by(EnterpriseId = eventFrameAttributeTemplate.EventFrameTemplate.origin().ElementTemplate.Site.Enterprise.EnterpriseId).order_by(Lookup.Name)
		form.lookup.query = lookupQuery
		firstLookup = lookupQuery.first()
		choices = []
		choices.append((-1, ""))
		for lookupValue in LookupValue.query.filter_by(LookupId = firstLookup.LookupId).order_by(LookupValue.Name):
			choices.append((lookupValue.Value, lookupValue.Name))

		form.defaultStartLookupValue.choices = choices
		form.defaultEndLookupValue.choices = choices
	else:
		modelName = "Event Frame Attribute Template"
		del form.defaultStartLookupValue
		del form.defaultEndLookupValue
		del form.lookup

	# Edit an existing eventFrameAttributeTemplate.
	if form.validate_on_submit():
		oldEventFrameAttributeTemplateName = eventFrameAttributeTemplate.Name
		eventFrameAttributeTemplate.Description = form.description.data
		eventFrameAttributeTemplate.Name = form.name.data

		if eventFrameAttributeTemplate.LookupId:
			eventFrameAttributeTemplate.DefaultEndValue = None if form.defaultEndLookupValue.data == -1 else form.defaultEndLookupValue.data
			eventFrameAttributeTemplate.DefaultStartValue = None if form.defaultStartLookupValue.data == -1 else form.defaultStartLookupValue.data
			eventFrameAttributeTemplate.Lookup = form.lookup.data
		else:
			eventFrameAttributeTemplate.DefaultEndValue = None if form.defaultEndValue.data is None else form.defaultEndValue.data,
			eventFrameAttributeTemplate.DefaultStartValue = None if form.defaultStartValue.data is None else form.defaultStartValue.data,
			eventFrameAttributeTemplate.UnitOfMeasurement = form.unitOfMeasurement.data

		db.session.commit()
		flash('You have successfully edited the event frame attribute template "{}".'.format(eventFrameAttributeTemplate.Name), "alert alert-success")
		createdTags = []
		updatedTags = []
		createdEventFrameAttributes = []
		updatedEventFrameAttributes = []
		for element in eventFrameAttributeTemplate.EventFrameTemplate.ElementTemplate.Elements:
			if element.isManaged():
				# Tag management.
				newTagName = "{}_{}".format(element.Name, eventFrameAttributeTemplate.Name.replace(" ", ""))
				oldTagName = "{}_{}".format(element.Name, oldEventFrameAttributeTemplateName.replace(" ", ""))
				oldTag = Tag.query.filter_by(AreaId = element.TagAreaId, Name = oldTagName).one_or_none()
				if oldTag is None:
					# Old tag doesn't exist.
					newTag = Tag.query.filter_by(AreaId = element.TagAreaId, Name = newTagName).one_or_none()
					if newTag is None:
						# New tag doesn't exist, so create it.
						tag = Tag(AreaId = element.TagAreaId, LookupId = eventFrameAttributeTemplate.LookupId, Name = newTagName,
							UnitOfMeasurementId = eventFrameAttributeTemplate.UnitOfMeasurementId)
						db.session.add(tag)
						db.session.commit()
						createdTags.append(tag)
						eventFrameAttributeTagId = tag.TagId
					else:
						# New tag exists, so update LookupId and UnitOfMeasurementId just in case.
						newTag.LookupId = eventFrameAttributeTemplate.LookupId
						newTag.UnitOfMeasurementId = eventFrameAttributeTemplate.UnitOfMeasurementId
						db.session.commit()
						updatedTags.append(newTag)
						eventFrameAttributeTagId = newTag.TagId
				else:
					# Old tag exists, so update LookupId, Name and UnitOfMeasurementId just in case.
					oldTag.LookupId = eventFrameAttributeTemplate.LookupId
					oldTag.Name = newTagName
					oldTag.UnitOfMeasurementId = eventFrameAttributeTemplate.UnitOfMeasurementId
					db.session.commit()
					updatedTags.append(oldTag)
					eventFrameAttributeTagId = oldTag.TagId

				# Event Frame attribute management.
				eventFrameAttribute = EventFrameAttribute.query.filter_by(ElementId = element.ElementId,
					EventFrameAttributeTemplateId = eventFrameAttributeTemplate.EventFrameAttributeTemplateId).one_or_none()
				if eventFrameAttribute is None:
					# The event frame attribute doesn't exist, so create it.
					eventFrameAttribute = EventFrameAttribute(ElementId = element.ElementId,
						EventFrameAttributeTemplateId = eventFrameAttributeTemplate.EventFrameAttributeTemplateId, TagId = eventFrameAttributeTagId)
					db.session.add(eventFrameAttribute)
					db.session.commit()
					createdEventFrameAttributes.append(eventFrameAttribute)
				else:
					# The event frame attribute exists, so update TagId just in case.
					eventFrameAttribute.TagId = eventFrameAttributeTagId
					db.session.commit()
					updatedEventFrameAttributes.append(eventFrameAttribute)


		createdTagsMessage = ""
		alert = "alert alert-success"
		if createdTags:
			createdTags.sort(key = lambda tag: tag.Name)
			for tag in createdTags:
				if createdTagsMessage == "":
					createdTagsMessage = 'Created the following tag(s):<br>"{}"'.format(tag.Name)
					alert = "alert alert-success"
				else:
					createdTagsMessage = '{}<br>"{}"'.format(createdTagsMessage, tag.Name)

			flash(createdTagsMessage, alert)

		updatedTagsMessage = ""
		if updatedTags:
			updatedTags.sort(key = lambda tag: tag.Name)
			for tag in updatedTags:
				if updatedTagsMessage == "":
					updatedTagsMessage = 'Updated the following existing tag(s), if needed:<br>"{}"'.format(tag.Name)
					alert = "alert alert-warning"
				else:
					updatedTagsMessage = '{}<br>"{}"'.format(updatedTagsMessage, tag.Name)

			flash(updatedTagsMessage, alert)

		createdEventFrameAttributesMessage = ""
		if createdEventFrameAttributes:
			createdEventFrameAttributes.sort(key = lambda eventFrameAttribute: eventFrameAttribute.Element.Name)
			for eventFrameAttribute in createdEventFrameAttributes:
				if createdEventFrameAttributesMessage == "":
					createdEventFrameAttributesMessage = 'Created the following element attribute(s):<br>Element: "{}" attribute: "{}" associated with tag: "{}"'. \
						format(eventFrameAttribute.Element.Name, eventFrameAttribute.EventFrameAttributeTemplate.Name, eventFrameAttribute.Tag.Name)
					alert = "alert alert-success"
				else:
					createdEventFrameAttributesMessage = '{}<br>Element: "{}" attribute: "{}" associated with tag: "{}"'.format(createdEventFrameAttributesMessage,
						eventFrameAttribute.Element.Name, eventFrameAttribute.EventFrameAttributeTemplate.Name, eventFrameAttribute.Tag.Name)

			flash(createdEventFrameAttributesMessage, alert)

		updatedEventFrameAttributesMessage = ""
		if updatedEventFrameAttributes:
			updatedEventFrameAttributes.sort(key = lambda eventFrameAttribute: eventFrameAttribute.Element.Name)
			for eventFrameAttribute in updatedEventFrameAttributes:
				if updatedEventFrameAttributesMessage == "":
					updatedEventFrameAttributesMessage = "Updated the following element attribute(s), if needed:<br>Element: " + \
						'"{}" attribute: "{}" associated with tag: "{}"'.format(eventFrameAttribute.Element.Name, eventFrameAttribute.EventFrameAttributeTemplate.Name,
						eventFrameAttribute.Tag.Name)
					alert = "alert alert-warning"
				else:
					updatedEventFrameAttributesMessage = '{}<br>Element: "{}" attribute: "{}" associated with tag: "{}"'.format(updatedEventFrameAttributesMessage,
						eventFrameAttribute.Element.Name, eventFrameAttribute.EventFrameAttributeTemplate.Name, eventFrameAttribute.Tag.Name)

			flash(updatedEventFrameAttributesMessage, alert)

		return redirect(form.requestReferrer.data)

	# Present a form to edit an existing eventFrameAttributeTemplate.
	form.eventFrameAttributeTemplateId.data = eventFrameAttributeTemplate.EventFrameAttributeTemplateId
	form.description.data = eventFrameAttributeTemplate.Description
	form.eventFrameTemplateId.data = eventFrameAttributeTemplate.EventFrameTemplateId
	form.name.data = eventFrameAttributeTemplate.Name
	if eventFrameAttributeTemplate.LookupId:
		form.defaultEndLookupValue.data = eventFrameAttributeTemplate.DefaultEndValue
		form.defaultStartLookupValue.data = eventFrameAttributeTemplate.DefaultStartValue
		form.lookup.data = eventFrameAttributeTemplate.Lookup
	else:
		form.defaultEndValue.data = eventFrameAttributeTemplate.DefaultEndValue
		form.defaultStartValue.data = eventFrameAttributeTemplate.DefaultStartValue
		form.unitOfMeasurement.data = eventFrameAttributeTemplate.UnitOfMeasurement

	if form.requestReferrer.data is None:
		form.requestReferrer.data = request.referrer

	if eventFrameAttributeTemplate.EventFrameTemplate.hasParent():
		breadcrumbs = [{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "Root"), "text" : "<span class = \"glyphicon glyphicon-home\"></span>"},
			{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "Enterprise",
				selectedId = eventFrameAttributeTemplate.EventFrameTemplate.origin().ElementTemplate.Site.Enterprise.EnterpriseId),
				"text" : eventFrameAttributeTemplate.EventFrameTemplate.origin().ElementTemplate.Site.Enterprise.Name},
			{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "Site",
				selectedId = eventFrameAttributeTemplate.EventFrameTemplate.origin().ElementTemplate.Site.SiteId),
				"text" : eventFrameAttributeTemplate.EventFrameTemplate.origin().ElementTemplate.Site.Name},
			{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "ElementTemplate",
				selectedId = eventFrameAttributeTemplate.EventFrameTemplate.origin().ElementTemplate.ElementTemplateId),
				"text" : eventFrameAttributeTemplate.EventFrameTemplate.origin().ElementTemplate.Name}]
		for eventFrameTemplateAcestor in eventFrameAttributeTemplate.EventFrameTemplate.ancestors([]):
			breadcrumbs.append({"url" : url_for("eventFrames.selectEventFrame", selectedClass = "EventFrame",
				selectedId = eventFrameTemplateAcestor.EventFrameTemplateId), "text" : eventFrameTemplateAcestor.Name})

		breadcrumbs.extend([{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "EventFrame",
			selectedId = eventFrameAttributeTemplate.EventFrameTemplate.EventFrameTemplateId),
			"text" : eventFrameAttributeTemplate.EventFrameTemplate.Name}, {"url" : None, "text" : eventFrameAttributeTemplate.Name}])
	else:
		breadcrumbs = [{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "Root"), "text" : "<span class = \"glyphicon glyphicon-home\"></span>"},
			{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "Enterprise",
				selectedId = eventFrameAttributeTemplate.EventFrameTemplate.ElementTemplate.Site.Enterprise.EnterpriseId),
				"text" : eventFrameAttributeTemplate.EventFrameTemplate.ElementTemplate.Site.Enterprise.Name},
			{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "Site",
				selectedId = eventFrameAttributeTemplate.EventFrameTemplate.ElementTemplate.Site.SiteId),
				"text" : eventFrameAttributeTemplate.EventFrameTemplate.ElementTemplate.Site.Name},
			{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "ElementTemplate",
				selectedId = eventFrameAttributeTemplate.EventFrameTemplate.ElementTemplate.ElementTemplateId),
				"text" : eventFrameAttributeTemplate.EventFrameTemplate.ElementTemplate.Name},
			{"url" : url_for("eventFrames.selectEventFrame", selectedClass = "EventFrameTemplate",
				selectedId = eventFrameAttributeTemplate.EventFrameTemplate.EventFrameTemplateId, selectedOperation = "configure"),
				"text" : eventFrameAttributeTemplate.EventFrameTemplate.Name},
			{"url" : None, "text" : eventFrameAttributeTemplate.Name}]

	return render_template("addEdit.html", breadcrumbs = breadcrumbs, form = form, modelName = modelName, operation = operation)
