from tpdb.BaseSceneScraper import BaseSceneScraper
from tpdb.items import SceneItem
import re
import scrapy
import imgkit
import os
import base64
import tempfile
from io import BytesIO
from PIL import Image


class SiteGirlsBoardingSchoolSpider(BaseSceneScraper):
    name = 'GirlsBoardingSchool'
    network = 'Girls Boarding School'
    parent = 'Girls Boarding School'
    site = 'Girls Boarding School'

    start_urls = [
        'https://girls-boarding-school.com',
    ]

    selector_map = {
        'pagination': '/new/%s',
        'external_id': ''
    }

    known_tags = {
            "belt",
            "birch",
            "brush",
            "cane",
            "carpetbeater",
            "coathanger",
            "hairbrush",
            "hand",
            "kneeling in peas",
            "leather paddle",
            "otk",
            "palm and feet spanking",
            "ruler",
            "slipper",
            "tawse",
            "unusual implements",
            "various",
            "wooden paddle",
            }


    def get_scenes(self, response):
        scenes = response.xpath('//div[contains(@class, "productionWrap")]')
        #print(str(scenes))
        scenelist = []
        for scene in scenes:
            item = SceneItem()
            #print(str(scene.get()))

            item['title'] = scene.xpath('.//h2[contains(@class, "mobileTitle")]/text()').get()
            item['description'] = scene.xpath('.//div[contains(@class, "productionDetailsDescription")]/text()').get() or ''
            item['site'] = "Girls Boarding School"
            item['date'] = None
            #item['image'] = 'http://bad.url'
            item['image'] = ''
            #previewGridNode = scene.xpath('.//span[contains(@class, "previewGridGrid")]').get()
            previewGrid = scene.xpath('.//span[contains(@class, "previewGridGrid")]').get()
            previewGrid = previewGrid.replace('src="data:image/png;base64', 'bad-src="data:image/png;base64')
            if 'data-imglg ' in previewGrid or "data-imglg=''" in previewGrid or 'data-imglg=""' in previewGrid:
                previewGrid = previewGrid.replace('data-echo="', 'src="https://www.girls-boarding-school.com')
            else:
                previewGrid = previewGrid.replace('data-imglg="', 'src="https://www.girls-boarding-school.com')
            #print(previewGrid)
            
            #Compose the html document
            imageDoc = '<!doctypehtml><title>title</title><meta content="width=device-width,initial-scale=1"name=viewport><style>.thumbWrap{display:block;float:left;position:relative;overflow:hidden}.imgRatioWrap{display:block;background:#111;position:relative;height:0;overflow:hidden;width:100%}.imgRatioWrap img{position:absolute;top:0;left:0;width:100%;height:100%;display:block}</style><body class=public style=margin:0px>' + previewGrid + '</body></html>'
            #print(imageDoc)

            fd, tempImageFileName = tempfile.mkstemp(prefix="gbsimg", suffix=".png")
            os.fdopen(fd).close()
            try:

                imgkit.from_string(imageDoc, tempImageFileName, {'format': 'png', 'crop-w': '800'})
                f = open(tempImageFileName, mode='rb')
                try:
                    data = f.read()
                    try:
                        img = BytesIO(data)
                        img = Image.open(img)
                        img = img.convert('RGB')
                        width, height = img.size
                        #if height > 1080 or width > 1920:
                            #img.thumbnail((1920, 1080))
                        buffer = BytesIO()
                        img.save(buffer, format="JPEG")
                        data = buffer.getvalue()
                    except Exception as ex:
                        print(f"Could not decode image for evaluation: '{image}'.  Error: ", ex)
                    item['image_blob'] = base64.b64encode(data).decode('utf-8') 
                finally:
                    f.close()
            finally:
                #print("os.remove(tempImageFileName)")
                os.remove(tempImageFileName)

            tags = list(map(lambda x : str(x.get()).strip(), scene.xpath('.//span[contains(@class, "productionTag") and not(contains(@class, "media"))]/span/text()')))
            #print(str(tags))
            

            item['performers'] = list(filter(lambda x : x.lower() not in self.known_tags, tags))
            item['tags'] = list(filter(lambda x : x.lower() in self.known_tags, tags))
            item['markers'] = None
            imgUrl = scene.xpath('(.//img[contains(@data-echo, "/prod")])[1]/@data-echo').get()
            item['id'] = str(int(re.search(r'/prod(\d+)', imgUrl).group(1))).zfill(4)
            #print("id is " + str(item['id']) + "\n")
            item['trailer'] = ''
            item['duration'] = None
            #the scenes don't have urls so just make something up
            item['url'] = 'https://girls-boarding-school.com/' + item['id']
            item['network'] = "Girls Boarding School"
            item['parent'] = "Girls Boarding School"
            item['type'] = 'Scene'
            yield self.check_item(item)
