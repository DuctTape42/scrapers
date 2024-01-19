import scrapy
from tpdb.BasePerformerScraper import BasePerformerScraper
from tpdb.items import PerformerItem


def get_birthday_from_age(age):
    age = int(age.strip())
    if age >= 18 and age <= 99:
        birthdate = datetime.now() - relativedelta(years=age)
        birthdate = birthdate.strftime('%Y-%m-%d')
        return birthdate
    return ''

class GirlsBoardingSchoolPerformerSpider(BasePerformerScraper):
    selector_map = {
        'name': '//div[contains(@class, "modelsWrapInner")]/span[@data-mname]//span[contains(@class, "modelName")]/text()',
        'image': '//div[contains(@class, "modelsWrapInner")]/span[@data-mname]/span/img/@src',
        'pagination': '',
        'external_id': '//div[contains(@class, "modelsWrapInner")]/span[@data-mname]//span[contains(@class, "modelName")]/text()',
    }

    name = 'GirlsBoardingSchoolPerformer'
    network = 'Girls Boarding School'
    parent = 'Girls Boarding School'

    start_urls = [
        'http://www.girls-boarding-school.com/new/models'
    ]

    def get_next_page_url(self, url, page):
        print(str(url))
        if page == 1:
            return url
        else:
            return None

    def get_performers(self, response):
        performers = response.xpath('//div[contains(@class, "modelsWrapInner")]/span[@data-mname]')
        items = []
        for performer in performers:
            item = PerformerItem()
            item['name'] = self.cleanup_title(performer.xpath('.//span[contains(@class, "modelName")]/text()').get())
            item['image'] = "https://www.girls-boarding-school.com" + performer.xpath('./span/img/@data-echo').get()
            print(item['image'])
            item['image_blob'] = self.get_image_blob_from_link(item['image'])
            print(item['image_blob'])
            item['gender'] = 'Female'
            item['network'] = self.network
            #these don't have urls so use the image
            item['url'] = item['image']
            item['bio'] = ''
            item['astrology'] = ''
            item['birthday'] = ''
            item['birthplace'] = ''
            item['cupsize'] = ''
            item['ethnicity'] = ''
            item['nationality'] = ''
            item['haircolor'] = ''
            item['eyecolor'] = ''
            item['weight'] = ''
            item['height'] = ''
            item['measurements'] = ''
            item['tattoos'] = ''
            item['piercings'] = ''
            item['fakeboobs'] = ''
            items.append(item)
        return items
