import cgi

import xml.etree.ElementTree as ET
import lead_record


def wrap(marketo_id=None, email=None, marketo_cookie=None, foreign_id=None, attributes=()):
    tmpl = u"<attribute>" \
           u"<attrName>{name}</attrName>" \
           u"<attrType>{typ}</attrType>" \
           u"<attrValue>{value}</attrValue>" \
           u"</attribute>"
    attr = "".join(tmpl.format(name=name, typ=typ, value=value) for name, typ, value in attributes)

    return u"<mkt:paramsSyncLead>" \
           u"<leadRecord>" \
           u"{marketo_id}" \
           u"{email}" \
           u"{foreign_id}" \
           u"<leadAttributeList>{attributes}</leadAttributeList>" \
           u"</leadRecord>" \
           u"<returnLead>true</returnLead>" \
           u"{marketo_cookie}" \
           u"</mkt:paramsSyncLead>".format(marketo_id="<Id>{0}</Id>".format(marketo_id) if marketo_id else "",
                                           email="<Email>{0}</Email>".format(email) if email else "",
                                           foreign_id="<ForeignSysPersonId>{0}</ForeignSysPersonId>"
                                                      "<ForeignSysType>CUSTOM</ForeignSysType>".format(foreign_id) if foreign_id else "",
                                           attributes=attr,
                                           marketo_cookie="<marketoCookie>{0}</marketoCookie>".format(cgi.escape(marketo_cookie)) if marketo_cookie else "")


def unwrap(response):
    root = ET.fromstring(response)
    lead_record_xml = root.find('.//leadRecord')
    return lead_record.unwrap(lead_record_xml)
