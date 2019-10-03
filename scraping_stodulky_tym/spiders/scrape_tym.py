# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scraping_stodulky_tym.items import ScrapingStodulkyItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose


class ScrapeTymSpider(CrawlSpider):
    name = 'scrape_tym'
    allowed_domains = ['www.fotbalpraha.cz']
    start_urls = ["https://www.fotbalpraha.cz/souteze/zapasy/75-a2b-1-a-trida-skupina-b-muzu?id_season=2018&id_team=26&id_round=999",
                    "https://www.fotbalpraha.cz/souteze/zapasy/76-a3a-1-b-trida-skupina-a-muzu?id_season=2018&id_team=26&id_round=999",
                  "https://www.fotbalpraha.cz/souteze/zapasy/84-c1a-prebor-starsiho-dorostu?id_season=2018&id_team=26&id_round=999",
                  "https://www.fotbalpraha.cz/souteze/zapasy/91-e2b-1-trida-skupina-b-starsich-zaku?id_season=2018&id_team=26&id_round=999",
                  "https://www.fotbalpraha.cz/souteze/zapasy/94-f1a-prebor-mladsich-zaku?id_season=2018&id_team=26&id_round=999",
                  "https://www.fotbalpraha.cz/souteze/zapasy/96-f2b-1-trida-skupina-b-mladsich-zaku?id_season=2018&id_team=26&id_round=999",
                  "https://www.fotbalpraha.cz/souteze/zapasy/97-f3a-2-trida-skupina-a-mladsich-zaku?id_season=2018&id_team=26&id_round=999"
                  ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@class="btn btn--white btn--no-margin"]'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
            vysledek_konec=response.xpath('//div[contains(@class, "game__scoreboard-score")]/text()').extract() #normalize-space v xpath maže mezery a řádky ve výsledném textu
            vysledek_polocas=response.css("div.game__scoreboard-score").css("span::text").extract()
            vysledek=vysledek_konec[0].strip()+" "+vysledek_polocas[0].strip()
            kiv=response.xpath('//div[contains(@class, "game__roster game__roster--top")]')
            sestava_domacich=kiv.css("div.game__roster-item").css("a::text").extract()[:11]
            sestava_d=", ".join(sestava_domacich) 
            sestava_hoste=kiv.css("div.game__roster-item").css("a::text").extract()[11:]
            sestava_h=", ".join(sestava_hoste) 
            goly=response.xpath('//div[contains(@class, "table-responsive game__timeline")]').xpath('//i[contains(@class, "ico ico-goal")]/following-sibling::a[1]/text()').extract()
            nahradnici_d=response.css('div.game__roster')[1].css("div.col-12")[0].css("div.game__roster-item").css("a::text").extract()
            nahradnici_d=", ".join(nahradnici_d)
            nahradnici_h=response.css('div.game__roster')[1].css("div.col-12")[1].css("div.game__roster-item").css("a::text").extract()
            nahradnici_h=", ".join(nahradnici_h)
            sestava_sokol=response.css("div.game__scoreboard").css("span.long::text").extract_first()
            soutez=response.xpath('//div[contains(@class, "game__league")]//a/text()').extract()[0]
            kolo=response.xpath('//div[@class="game__info"]//b/text()').extract()[0]
            poradi=kolo.find(".")
            kolo=kolo[:poradi]
            datum_cas=response.xpath('//div[@class="game__info"]//b/text()').extract()[1:3]
            souper1=response.css("div.game__scoreboard-team")[0].css("span.middle::text").extract()
            souper2=response.css("div.game__scoreboard-team")[1].css("span.middle::text").extract()
            souperi=souper1[0]+" - "+souper2[0]
            listy=[]
            listy2=[]
            for i in goly:
                if (i in sestava_domacich) or (i in nahradnici_d):
                    listy.append(i)
                else:
                    listy2.append(i)
            listy=", ".join(listy)
            listy2=", ".join(listy2)
            if "Stodůlky" in sestava_sokol:
                    if listy==[]:
                        l=ItemLoader(item=ScrapingStodulkyItem(), response=response)
                        l.add_value("Soutěž", soutez)
                        l.add_value("Kolo",kolo)
                        l.add_value("Datum_a_čas_utkání",datum_cas)
                        l.add_value("Soupeři", souperi)
                        l.add_value("Výsledek_utkání", vysledek)
                        l.add_value("Sestava", sestava_d)
                        l.add_value("Góly_Sokola", "bez vstřeleného gólu")
                        l.add_value("Náhradníci", nahradnici_d)
                        return l.load_item()
                    else:
                        l=ItemLoader(item=ScrapingStodulkyItem(), response=response)
                        l.add_value("Soutěž", soutez)
                        l.add_value("Kolo",kolo)
                        l.add_value("Datum_a_čas_utkání",datum_cas)
                        l.add_value("Soupeři", souperi)
                        l.add_value("Výsledek_utkání", vysledek)
                        l.add_value("Sestava", sestava_d)
                        l.add_value("Góly_Sokola", listy)
                        l.add_value("Náhradníci", nahradnici_d)
                        return l.load_item()
            else:
                    if listy2==[]:
                        l=ItemLoader(item=ScrapingStodulkyItem(), response=response)
                        l.add_value("Soutěž", soutez)
                        l.add_value("Kolo",kolo)
                        l.add_value("Datum_a_čas_utkání",datum_cas)
                        l.add_value("Soupeři", souperi)
                        l.add_value("Výsledek_utkání", vysledek)
                        l.add_value("Sestava", sestava_h)
                        l.add_value("Góly_Sokola", "bez vstřeleného gólu")
                        l.add_value("Náhradníci", nahradnici_h)
                        return l.load_item()
                    else:
                        l=ItemLoader(item=ScrapingStodulkyItem(), response=response)
                        l.add_value("Soutěž", soutez)
                        l.add_value("Kolo",kolo)
                        l.add_value("Datum_a_čas_utkání",datum_cas)
                        l.add_value("Soupeři", souperi)
                        l.add_value("Výsledek_utkání", vysledek)
                        l.add_value("Sestava", sestava_h)
                        l.add_value("Góly_Sokola", listy2)
                        l.add_value("Náhradníci", nahradnici_h)
                        return l.load_item()

