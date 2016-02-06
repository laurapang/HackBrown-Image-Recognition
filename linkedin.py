import json
from scrapy import Spider, Item, Field
from scrapy.spiders.init import InitSpider
from scrapy.http import Request, FormRequest

class Person(Item):
    '''
    Target fields that we wish to scrap
    '''
    link = Field()
    name = Field()
    location = Field()
    industry = Field()
    company = Field()
    previous = Field()
    education = Field()
    # connected_on = Field()
    title = Field()
    email = Field()
    sites = Field()
    twitter = Field()
    phone_numbers = Field()

class LinkedPySpider(InitSpider):
    name = 'LinkedPySpider'
    allowed_domains = ['linkedin.com']
    login_page = 'https://www.linkedin.com/uas/login'
    login_info = { 'session_key': 'aaronGokaslan@gmail.com',
                   'session_password': 'T0psecret'}
    start_urls = ["https://www.linkedin.com/contacts/api/contacts/"]

   # def __init__(self, **kwargs):
        #self.login_info['session_key'] = kwargs.get('id')
        #self.login_info['session_password'] = kwargs.get('pass')

    def init_request(self):
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        return FormRequest.from_response(response,
                    formdata=self.login_info,
                    callback=self.check_login_response)

    def check_login_response(self, response):
        if "Sign Out" in response.body:
            print("Logged in")
            for url in self.start_urls: 
                print url
                yield Request(url=url, callback=self.parse_contact_list)
        else:
            print("Open up linkedin.py, change line 28 with your linked in email & password.")

    def parse_contact_list(self, response):
        '''
        Scrap connection list 
        '''

        connections = (json.loads(response.body))["contacts"]  
        for connection in connections:
            print connection['id']
            # for each connection, get the detailed api page & basic profile page urls
            url = 'http://linkedin.com/contacts/view?id='+connection['id']
            url2 = 'https://www.linkedin.com/contacts/api/contacts/' + \
                    connection['id']+ \
                    '/?fields=name,emails_extended,birthday,phone_numbers,sites,'+ \
                    'addresses,company,title,location,ims,profiles,twitter,wechat,display_sources'
            yield Request(url=url, meta={'detail_url': url2}, callback=self.parse_basic)

    def parse_basic(self, response):
        '''
        Scrap basic details for person
        '''
        person = Person()
        person['name'] = response.xpath('//span[@class="full-name"]/text()').extract()
        person['industry'] = response.xpath('//dd[@class="industry"]/a/text()').extract()
        person['company'] = response.xpath('//div[@id="headline"]/p[@class="title"]/text()').extract()
        person['education'] = response.xpath('//tr[@id="overview-summary-education"]/td/ol/li/a/text()').extract()
        # person['connected_on'] = response.xpath('//div[@class="item-info grey-txt"]').extract()
        previous = response.xpath('//tr[@id="overview-summary-past"]/td/ol')
        if (previous):
            person['previous'] = (previous[0].xpath('.//li//text()').extract())
            person['previous'] = "".join(person['previous'])

        yield Request(url=response.meta['detail_url'], meta={'person':person}, callback=self.parse_detail)

    def parse_detail(self, response):
        '''
        Scrap detailed information for person
        '''
        json_obj = (json.loads(response.body))["contact_data"]
        person = response.meta['person']

        try:
            person['email'] = json_obj["emails_extended"][0]["email"]  
        except:
            pass
        try:
            person['link'] = json_obj["profiles"][0]['url']
        except:
            pass
        try:
            person['twitter'] = json_obj['twitter'][0]['url']
        except:
            pass

        sites = json_obj['sites']
        person['sites'] = []
        for i in sites:
            person['sites'].append(i['url'])

        phone_numbers = json_obj['phone_numbers']
        person['phone_numbers'] = []
        for i in phone_numbers:
            person['phone_numbers'].append(i['number'])
            
        person['location'] = json_obj['location']
        person['title'] = json_obj['title']

        # finished with this person
        return person

