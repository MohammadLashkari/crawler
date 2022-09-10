# Mohammad Lashkari - 98149053

import scrapy

class GooglePlaySpider(scrapy.Spider):

    name = "google_play"

    allowed_domains = ["play.google.com"]

    start_urls = [
        "https://play.google.com/store/apps/details?id=com.activision.callofduty.shooter"
    ]

    # Delay To Requests
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }
    # Spider Depth Level
    depth_limit = 3

    def parse(self, response):
        for game in response.css("div.T4LgNb"):
            yield {
                "Game Name": game.css("h1.AHFaub span::text").get(),
                "Creator": game.css("div.qQKdcc a::text").get(),
                "Genre": game.css("div.qQKdcc a::text")[1].get(),
                "Age Limit": game.css("div.IQ1z0d span.htlgb div::text")[0].get(),
                "Violence Level": game.css("div.IQ1z0d span.htlgb div::text")[1].get(),
                "Rating": game.css("div.BHMmbe::text").get(),
                "Number of Reviews": game.css("span.EymY4b span::text").get(),
                "Number of Installations": game.css("div.IQ1z0d span.htlgb::text")[2].get(),
                "Last Update" : game.css("div.IQ1z0d span.htlgb::text")[0].get(),
                "Current Version": game.css("div.IQ1z0d span.htlgb::text")[3].get(),
                "Requires Android": game.css("div.IQ1z0d span.htlgb::text")[4].get(),
                "Description": [item .strip() for item in game.css("div span div ::text").getall()],
                "Depth Level": response.meta.get("depth"),
            }

        next_pages = response.css("div.RZEgze a.JC71ub::attr(href)").getall()
        if next_pages is not None and response.meta.get("depth") < self.depth_limit:
            yield from response.follow_all(next_pages, callback=self.parse)

