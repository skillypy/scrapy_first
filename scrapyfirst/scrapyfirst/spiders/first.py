import scrapy


class FirstSpider(scrapy.Spider):
    name = 'first'
    # aktifkan docker RWID utk link ini
    allowed_domains = ['127.0.0.1']

    # mulai dari url disini
    start_urls = ['http://127.0.0.1:5000/']

    def parse(self, response):
        data = {
            'username': 'user',
            'password': 'user12345'
        }

        return scrapy.FormRequest(
            url='http://127.0.0.1:5000/login',
            formdata = data,
            callback=self.after_login
        )

    def after_login(self, response):
        """
        ada 2 tugas disini:
        1. ambil semua data barang yang ada di halaman hasil -> parsing detail
        2. ambil semua link next (pagination) -> akan balik ke self.after_login

        :param response:
        :return:
        """

        # 1. get detail products
        details = response.css('.card .card-title a')
        for detail in details:
            href = detail.attrib.get('href')
            yield response.follow(href, callback=self.parse_detail)

        # 2. get all url product
        pagination = response.css('.pagination a.page-link')
        for pages in pagination:
            href = pages.attrib.get('href')
            yield response.follow(href, callback=self.after_login)


    def parse_detail(self, response):
        image = response.css('.card-img-top').attrib.get('src')
        title = response.css('.card-title::text').get()
        stock = response.css('.card-stock::text').get()
        desc = response.css('.card-text::text').get()

        return {
            'image': image,
            'title': title,
            'stock': stock,
            'desc': desc,
        }
