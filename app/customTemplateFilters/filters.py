from flask import current_app
from sqlalchemy import func
from . import customTemplateFilters
from .. models import Element, ElementTemplate, EventFrame, EventFrameTemplate, Site

@customTemplateFilters.app_template_filter()
def grafanaUrl(uid, parameters = None):
    if uid == "":
        return "http://{}:{}".format(current_app.config["GRAFANA_HOSTNAME"], current_app.config["GRAFANA_PORT"])
    elif uid == "ActiveEventFrameSummary":
        if "elementTemplateId" in parameters:
            elementTemplate = ElementTemplate.query.get_or_404(parameters["elementTemplateId"])
            return "http://{}:{}".format(current_app.config["GRAFANA_HOSTNAME"], current_app.config["GRAFANA_PORT"]) + \
                "/d/ActiveEventFrameSummary/active-event-frame-summary?orgId=1" + \
                "&var-enterprise={}".format(elementTemplate.Site.Enterprise.EnterpriseId) + \
                "&var-site={}".format(elementTemplate.Site.SiteId) + \
                "&var-elementTemplates={}".format(elementTemplate.ElementTemplateId) + \
                "&var-eventFrameTemplates=All" + \
                "&var-eventFrameAttributeTemplates=All"
        elif "eventFrameTemplateId" in parameters:
            eventFrameTemplate = EventFrameTemplate.query.get_or_404(parameters["eventFrameTemplateId"])
            return "http://{}:{}".format(current_app.config["GRAFANA_HOSTNAME"], current_app.config["GRAFANA_PORT"]) + \
                "/d/ActiveEventFrameSummary/active-event-frame-summary?orgId=1" + \
                "&var-enterprise={}".format(eventFrameTemplate.ElementTemplate.Site.Enterprise.EnterpriseId) + \
                "&var-site={}".format(eventFrameTemplate.ElementTemplate.Site.SiteId) + \
                "&var-elementTemplates={}".format(eventFrameTemplate.ElementTemplate.ElementTemplateId) + \
                "&var-eventFrameTemplates={}".format(eventFrameTemplate.EventFrameTemplateId) + \
                "&var-eventFrameAttributeTemplates=All"
        elif "siteId" in parameters:
            site = Site.query.get_or_404(parameters["siteId"])
            return "http://{}:{}".format(current_app.config["GRAFANA_HOSTNAME"], current_app.config["GRAFANA_PORT"]) + \
                "/d/ActiveEventFrameSummary/active-event-frame-summary?orgId=1" + \
                "&var-enterprise={}".format(site.Enterprise.EnterpriseId) + \
                "&var-site={}".format(site.SiteId) + \
                "&var-elementTemplates=All" + \
                "&var-eventFrameTemplates=All" + \
                "&var-eventFrameAttributeTemplates=All"
    elif uid == "ElementSummary":
        if "siteId" in parameters:
            site = Site.query.get_or_404(parameters["siteId"])
            return "http://{}:{}".format(current_app.config["GRAFANA_HOSTNAME"], current_app.config["GRAFANA_PORT"]) + \
                "/d/ElementSummary/element-summary?orgId=1" + \
                "&var-enterprise={}".format(site.Enterprise.EnterpriseId) + \
                "&var-site={}".format(parameters["siteId"]) + \
                "&var-elementTemplates=All" + \
                "&var-elements=All" + \
                "&var-elementAttributeTemplates=All"
        elif "elementTemplateId" in parameters:
            elementTemplate = ElementTemplate.query.get_or_404(parameters["elementTemplateId"])
            elements = ""
            for element in elementTemplate.Elements:
                elements += "&var-elements={}".format(element.ElementId)
            return "http://{}:{}".format(current_app.config["GRAFANA_HOSTNAME"], current_app.config["GRAFANA_PORT"]) + \
                "/d/ElementSummary/element-summary?orgId=1" + \
                "&var-enterprise={}".format(elementTemplate.Site.Enterprise.EnterpriseId) + \
                "&var-site={}".format(elementTemplate.Site.SiteId) + \
                "&var-elementTemplates={}".format(elementTemplate.ElementTemplateId) + \
                elements + \
                "&var-elementAttributeTemplates=All"
    elif uid == "ElementValuesGraph":
        element = Element.query.get_or_404(parameters["elementId"])
        return "http://{}:{}".format(current_app.config["GRAFANA_HOSTNAME"], current_app.config["GRAFANA_PORT"]) + \
            "/d/ElementValuesGraph/element-values-graph?orgId=1" + \
            "&var-enterprise={}".format(element.ElementTemplate.Site.Enterprise.EnterpriseId) + \
            "&var-site={}".format(element.ElementTemplate.Site.SiteId) + \
            "&var-elementTemplates=All" + \
            "&var-elements={}".format(parameters["elementId"]) + \
            "&var-elementAttributeTemplates=All" + \
            "&var-lookups=All"
    elif uid == "EventFramesGraph":
        eventFrame = EventFrame.query.get_or_404(parameters["eventFrameId"])
        startTimestamp = EventFrame.query.with_entities(func.unix_timestamp(EventFrame.StartTimestamp)).filter_by(EventFrameId = eventFrame.EventFrameId). \
            one()[0]
        if eventFrame.EndTimestamp:
            endTimestamp = EventFrame.query.with_entities(func.unix_timestamp(EventFrame.EndTimestamp)).filter_by(EventFrameId = eventFrame.EventFrameId). \
                one()[0]
            return "http://{}:{}".format(current_app.config["GRAFANA_HOSTNAME"], current_app.config["GRAFANA_PORT"]) + \
                "/d/EventFramesGraph/event-frames-graph?orgId=1" + \
                "&from={}000".format(startTimestamp) + \
                "&to={}000".format(endTimestamp) + \
                "&var-enterprise={}".format(eventFrame.EventFrameTemplate.ElementTemplate.Site.Enterprise.EnterpriseId) + \
                "&var-site={}".format(eventFrame.EventFrameTemplate.ElementTemplate.Site.SiteId) + \
                "&var-elementTemplate={}".format(eventFrame.EventFrameTemplate.ElementTemplate.ElementTemplateId) + \
                "&var-eventFrameTemplate={}".format(eventFrame.EventFrameTemplate.EventFrameTemplateId) + \
                "&var-eventFrame={}".format(parameters["eventFrameId"]) + \
                "&var-eventFrameAttributeTemplates=All" + \
                "&var-lookups=All"
        else:
            return "http://{}:{}".format(current_app.config["GRAFANA_HOSTNAME"], current_app.config["GRAFANA_PORT"]) + \
                "/d/EventFramesGraph/event-frames-graph?orgId=1" + \
                "&from={}000".format(startTimestamp) + \
                "&to=now" + \
                "&var-enterprise={}".format(eventFrame.EventFrameTemplate.ElementTemplate.Site.Enterprise.EnterpriseId) + \
                "&var-site={}".format(eventFrame.EventFrameTemplate.ElementTemplate.Site.SiteId) + \
                "&var-elementTemplate={}".format(eventFrame.EventFrameTemplate.ElementTemplate.ElementTemplateId) + \
                "&var-eventFrameTemplate={}".format(eventFrame.EventFrameTemplate.EventFrameTemplateId) + \
                "&var-eventFrame={}".format(parameters["eventFrameId"]) + \
                "&var-eventFrameAttributeTemplates=All" + \
                "&var-lookups=All"
    elif uid == "TagValuesGraph":
        return "http://{}:{}".format(current_app.config["GRAFANA_HOSTNAME"], current_app.config["GRAFANA_PORT"]) + \
            "/d/TagValuesGraph/tag-values-graph?orgId=1" + \
            "&var-enterprises=All" + \
            "&var-sites=All" + \
            "&var-areas=All" + \
            "&var-tags={}".format(parameters["tagId"]) + \
            "&var-lookups=All"
