import requests
from xml.etree import ElementTree

class Products:

  api_url = 'https://jvndb.jvn.jp/myjvn'

  base_query = {
    'method': 'getProductList',
    'feed': 'hnd',
  }

  def get(self):

    response = requests.get(self.api_url, params = self.base_query)
    xml = ElementTree.fromstring(response.content)
    products = []
    for vendor in xml[0]:
      product_dict = {
        'vendor_id': vendor.attrib['vid'],
        'vendor_name': vendor.attrib['vname'],
      }
      for product in vendor:
        product_dict['product_id'] = product.attrib['pid']
        product_dict['product_name'] = product.attrib['pname']
      products.append(product_dict)
    return products


    # print(xml[0]) # vendorInfo
    # print(xml[0][0]) # vendor
    # print(xml[0][0][0]) # product
    # print(xml[0][0][0].attrib['pname'])



# query = {
#   'method': 'getProductList',
#   'feed': 'hnd',
#   'keyword': 'WordPress'
# }
