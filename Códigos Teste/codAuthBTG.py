import json
import requests

payload = {
    'login': "11556539630",
    'password': "001122",
    'softToken': "705813",
    'type': "external"
} 

headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
           }


url ='https://access.btgpactualdigital.com/login/api/auth/token'

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    p = s.post(url, json=payload, headers=headers)
    tokenJWT = p.text

    payload2 = {
  "accountNumber": "001845285",
  "accountingGroupCode": "CRA",
  "fixedIncomeAcquisitions": [
    {
      "accountNumber": "null",
      "acquisitionDate": "2022-07-21T00:00:00.000-0300",
      "acquisitionQuantity": 980,
      "costPrice": 1023.231256,
      "grossValue": 1061702.69,
      "iofTax": 0,
      "incomeTax": 0,
      "initialInvestmentQuantity": 980,
      "initialInvestmentValue": 1002766.63,
      "netValue": 1061702.69,
      "positionDate": "2023-10-17T18:07:07.000-0300",
      "securityCode": "5479295",
      "yieldToMaturity": 7.1,
      "tradeId": 3402255,
      "interfaceDate": "2023-10-16T00:00:00.000-0300",
      "priceIncomeTax": 0,
      "priceVirtualIof": 0,
      "transferId": "16923586",
      "prices": [
        {
          "priceType": 200,
          "price": 1083.3700953767202,
          "incomeTax": 0,
          "iOFTax": 0
        },
        {
          "priceType": 9,
          "price": 1079.33138155,
          "incomeTax": 0,
          "iOFTax": 0
        }
      ]
    }
  ],
  "referenceIndexName": "IPCA",
  "ticker": "CRA-CRA022000XF",
  "yield": 7.1
}

    print(payload2)

    headers2 = {
           'Authorization': 'JWT ' + tokenJWT,
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        #    'Cookie': '_ga=GA1.1.715147548.1676038375; _hjSessionUser_2808211=eyJpZCI6IjEwYzZhZGJkLTM0OGYtNTFiMC1hMTRjLTg3MjhkOTQ5NGM3MCIsImNyZWF0ZWQiOjE2NzY1NTQyNTg5OTksImV4aXN0aW5nIjp0cnVlfQ==; rdtrk=%7B%22id%22%3A%223d11d015-3852-43f3-9694-764bbebb1224%22%7D; _ga_GT4CNBLG65=GS1.1.1678739006.3.1.1678739207.0.0.0; _ga_055MMTFXV7=GS1.1.1678739006.3.1.1678739207.60.0.0; __utmz=192726137.1678801261.5.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); liveagent_oref=https://access.btgpactualdigital.com/op/reports; liveagent_vc=2; liveagent_ptid=b73349e4-15ec-4b07-8dd1-8fc54db90777; _gcl_au=1.1.842052362.1692103372; _vwo_uuid_v2=D1B8F18AC5C12A1CA7AE20745F2D7B614|167908907ba5bcfa4f2fe17cef33e0e3; __utma=192726137.715147548.1676038375.1678801261.1692732121.6; _vwo_uuid=D1B8F18AC5C12A1CA7AE20745F2D7B614; _vwo_ds=3%241692732120%3A48.19076767%3A%3A; AMCV_8A2A1AAE589065BF0A495CC2%40AdobeOrg=359503849%7CMCIDTS%7C19592%7CMCMID%7C15364427456804882214425893998134543140%7CMCAAMLH-1693336984%7C4%7CMCAAMB-1693336984%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1692739384s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.0.1; AMCV_8A2A1AAE589065BF0A495CC2%40AdobeOrg=-1124106680%7CMCIDTS%7C19637%7CMCMID%7C15364427456804882214425893998134543140%7CMCAAMLH-1697208033%7C4%7CMCAAMB-1697208033%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1696610433s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.2.0; __utma=221004424.715147548.1676038375.1696603234.1696603234.1; __utmz=221004424.1696603234.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _vwo_uuid_v2=D1B8F18AC5C12A1CA7AE20745F2D7B614|167908907ba5bcfa4f2fe17cef33e0e3; _uetvid=2bb074a0412111eea6d1410a07b56321; __trf.src=encoded_eyJmaXJzdF9zZXNzaW9uIjp7InZhbHVlIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJleHRyYV9wYXJhbXMiOnt9fSwiY3VycmVudF9zZXNzaW9uIjp7InZhbHVlIjoiaHR0cHM6Ly9hY2Nlc3MuYnRncGFjdHVhbGRpZ2l0YWwuY29tL3NlcnZpY2VzL3JvYm9hZHZpc29yL3B1YmxpYy9hdXRoIiwiZXh0cmFfcGFyYW1zIjp7fX0sImNyZWF0ZWRfYXQiOjE2OTY2MDMyMzQzMzh9; _clck=t4yj1l|2|ffm|0|1374; _vis_opt_s=2%7C; _wingify_pc_uuid=85ea3985f0504d9187430be149306910; wingify_donot_track_actions=0; _ga_288419063=GS1.1.1696603234.2.0.1696603237.0.0.0; _ga_9JPZP9B352=GS1.1.1696603234.9.0.1696603238.56.0.0; _ga=GA1.1.715147548.1676038375; _gid=GA1.1.1034175201.1697464819; bm_mi=0905DF0F650687CBFC171C1F27173593~YAAQLhc2F58nODmLAQAAV3pRPxUFja2ITKj4PsJtUSPf9TfO+Lr6cXnZpWSDNT1IX4LW5YLNGGsPPS8vQU2hPv4JFUXi7XBy2RWNG4ufbJxRK0qYnvqmhRmCzsYyNrWBwg527AlSJADmFqnfm7knydvtUZhvRwIOr/bnRyz33T50EFsQ+SsEToIuUS9+k6RuusslM4MAgQoUJ1UbS6uxBoBdm9WT0s+Cw+tOU33o0fU8b6HhWYmU1fxGIOnhYz8MfowiPrpe7NFlpovMBYk6OTT5ZlVRMvjs48bjM+XBEvjCQ6HX2Eq6RRjcWgwZ492lvz2a4xcPBTrY5LnNYOVGFxpb~1; bm_sv=28B238E1CCCF41AF4524F735FDCCFC58~YAAQLhc2Fz8oODmLAQAAH4NRPxUst0EJ9A3DN/DARZP+NN7w/rfnimBO15/0I12RibrjmHik9U2VYrdLpVhr3tqi6jRQoEQSL7sktI8M2C+VlhVN0UMNnh3prfL7peOavussuF/qrUsa+RFr3ewtTsNUWoOUAQSANIOiBA0Ekyi5tzFsunvspiQFKAhZPONz1HOlz8U5CMr1nIAY6+vYPn6Z6/aVHhd2CVJtv1Tibd8Evi6reIPIKZiwmFvJXwQADszrJNWnMkn6e5Ym~1; ak_bmsc=A83070BC3A7BFA35B67897D532B9A8F7~000000000000000000000000000000~YAAQLhc2F9ozODmLAQAAeWpSPxV9bN7CLNcJfwIegqd+I2lZHgOJ/ty2JMyWlI63IvtdI8oQ7j4l/3tDBAxwpiP7GZP5sPJ5jA0EGSG9CY2dtz69wnD0U42eA5IzBN5UhAT3QKzXDcB5Msif4IRAVnxwPfdpgAFq/kJ1GkFPEOySaALuS7hdFEd0aneCchQ1V/rdDXY8+1+4ekCczIUMxHJvPJyAASic/WSKPf3WmE13kiRAFiCyr4OzrbZlVz01ck6GQSvIwIigY1t6lJj+bz6RiT5+jxw3ZdAfxzP1u3e+xOl3NMS9y+9ABBbE7+beNRw/Pf87Zzn/yCEbf6bGktF0khLCmRy3YWpKMu6fR7n5kqhKobaiUowsjxylTjIi2lkI51TbST3eidG2MvP3+Zu6CWpPfKcyOkXcB1lSIddd3lF+IyNsMsZ8l3tsO4mwF3HanrU=; _ga_14QBVL1P8G=GS1.1.1697570943.281.1.1697576826.2.0.0; _dd_s=rum=1&id=cbd43496-84f0-4da8-9dfd-b957c9368693&created=1697571082832&expire=1697577747881',
        #     'Origin': 'https://access.btgpactualdigital.com',
        #    'Referer': 'https://access.btgpactualdigital.com/op/clients/01408975696/portifolio/001845285/position'

           }

    url2 = 'https://access.btgpactualdigital.com/op/api/rmadmin/indicatives/settlement'
    r = requests.post(url2, json=payload2, headers=headers2)
    print(r.text)