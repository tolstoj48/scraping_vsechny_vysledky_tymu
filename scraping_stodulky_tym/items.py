# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field



class ScrapingStodulkyItem(Item):
    Soutěž=Field()
    Kolo=Field()
    Datum_a_čas_utkání=Field()
    Soupeři=Field()
    Výsledek_utkání=Field()
    Sestava=Field()
    Góly_Sokola=Field()
    Náhradníci=Field()