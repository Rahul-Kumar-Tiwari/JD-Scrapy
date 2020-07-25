import scrapy


def extract_Phone_number(phone_string):
    phone = phone_string.split("-")
    mob_number_corros_char = []
    actual_phone_no = "+(91)-"
    for i in range(len(phone)):
        if i != 0:
            mob_number_corros_char.append(phone[i][:2])
    for i in mob_number_corros_char[6:]:
        if i == "ji":
            actual_phone_no += "9"
        elif i == "lk":
            actual_phone_no += "8"
        elif i == "nm":
            actual_phone_no += "7"
        if i == "po":
            actual_phone_no += "6"
        elif i == "rq":
            actual_phone_no += "5"
        elif i == "ts":
            actual_phone_no += "4"
        if i == "vu":
            actual_phone_no += "3"
        elif i == "wx":
            actual_phone_no += "2"
        elif i == "yz":
            actual_phone_no += "1"
        elif i == "acb":
            actual_phone_no += "0"

    return actual_phone_no


class JustdialScraper(scrapy.Spider):
    name = "JustdialScraper"
    main_url = "https://justdial.com/Delhi/House-On-Rent/nct-10192844/page-"


    def start_requests(self):
        for page_no in range(51):
            next_page = self.main_url + str(page_no)
            try:
                yield scrapy.Request(url=next_page, callback=self.parse)

            except IndexError:
                break

    def parse(self, response):
        Data = response.css(".colsp")

        for Jd_details in Data:
            name = Jd_details.css('span.lng_cont_name::text').extract()
            address = Jd_details.css('.cont_fl_addr::text').extract()
            contact_no = Jd_details.css(".mobilesv").extract()
            rating = Jd_details.css('span.green-box::text').extract()

            contact_number = extract_Phone_number(str(contact_no))
            yield {
                'name': name[0],
                "rating": rating[0],
                "phone": contact_number,
                "address": address[0]

            }