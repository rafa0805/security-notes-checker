import requests
from xml.etree import ElementTree
from repository.jvn.jvn_common import JvnCommon

class Vulnerabilities (JvnCommon):

  xmlns = 'http://purl.org/rss/1.0/'
  xmlns_sec = 'http://jvn.jp/rss/mod_sec/3.0/'
  xmlns_status="http://jvndb.jvn.jp/myjvn/Status"

  base_query = {
    'method': 'getVulnOverviewList',
    'feed': 'hnd',
  }

  def critical(self, public_start_date):
    query_params = self.base_query.copy()
    query_params['severity'] = 'c'
    query_params = self.set_query_date(query_params, public_start_date)
    return self.get_body(query_params)

  def important(self, public_start_date):
    query_params = self.base_query.copy()
    query_params['severity'] = 'h'
    query_params = self.set_query_date(query_params, public_start_date)
    return self.get_body(query_params)

  def warn(self, public_start_date):
    query_params = self.base_query.copy()
    query_params['severity'] = 'm'
    query_params = self.set_query_date(query_params, public_start_date)
    return self.get_body(query_params)

  def informative(self, public_start_date):
    query_params = self.base_query.copy()
    query_params['severity'] = 'l'
    query_params = self.set_query_date(query_params, public_start_date)
    return self.get_body(query_params)

  def set_query_date(self, query_params, public_start_date):
    query_params['publicStartY'] = public_start_date.year
    query_params['publicStartM'] = public_start_date.month
    query_params['publicStartD'] = public_start_date.day
    return query_params

  def get_body(self, query_params):
    response = requests.get(self.api_url, params = query_params)
    xml = ElementTree.fromstring(response.content)
    return self.parse_xml(xml)

  def parse_xml(self, xml):
    return self.make_vulnerability_list(xml) if self.has_vulnerability(xml) else []

  def has_vulnerability(self, xml):
    responseStatus = xml.find('{%s}Status' % self.xmlns_status)
    return not responseStatus.attrib['totalRes'] == '0'

  def make_vulnerability_list(self, xml):
    vulnerabilities = []
    for vuln in xml.findall('{%s}item' % self.xmlns):
      reference_nodes = vuln.findall('{%s}references' % self.xmlns_sec)
      severity_nodes = vuln.findall('{%s}cvss' % self.xmlns_sec)
      vuln_dict = {
        'id': vuln.find('{%s}identifier' % self.xmlns_sec).text,
        'title': vuln.find('{%s}title' % self.xmlns).text,
        'link': vuln.find('{%s}link' % self.xmlns).text,
        'description': vuln.find('{%s}description' % self.xmlns).text,
        'references': self.make_reference_list(reference_nodes),
        'cvss2': self.make_cvss_dict(ver = '2.0', severity_nodes = severity_nodes),
        'cvss3': self.make_cvss_dict(ver = '3.0', severity_nodes = severity_nodes),
      }
      vulnerabilities.append(vuln_dict)
    return vulnerabilities

  def make_reference_list(self, reference_nodes):
    refereces_list = []
    for ref in reference_nodes:
      refereces_list.append({
        'source': ref.attrib['source'] if 'source' in ref.attrib.keys() else None,
        'id': ref.attrib['id'],
        'link': ref.text,
        'title': ref.attrib['title'] if 'title' in ref.attrib.keys() else None,
      })
    return refereces_list

  def make_cvss_dict(self, ver, severity_nodes):
    cvss_xml = {}
    for node in severity_nodes:
      if node.attrib['version'] == ver:
        cvss_xml['score'] = node.attrib['score']
        cvss_xml['severity'] = node.attrib['severity']
        break
    return cvss_xml
