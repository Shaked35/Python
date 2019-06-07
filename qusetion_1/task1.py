import json


class AlbertContainer(object):
    FILE = 'ads.json'

    def main(self):
        with open(self.FILE) as json_file:
            ads = json.load(json_file)
        url_to_ags_list_by_name = self.divide_by_url_name(ads)
        url_to_ags_list_by_url = self.divide_by_url(url_to_ags_list_by_name)
        url_to_ags_list_by_image = self.divide_by_image(url_to_ags_list_by_url)
        # Final Complexity = n + n^2 + n^2 = O(n^2) - in the worst case
        print(url_to_ags_list_by_image)
    """
    This method divide the items by the url name
    Complexity = O(n)
    :return dictionary with key = url name values = list of (ag_id, ad_id)
    """
    @staticmethod
    def divide_by_url_name(ags_list):
        url_step1_to_ags_list = {}
        for ad in ags_list:
            temp_ad = (ad["ad_group_id"], ad["ad_id"])
            url_step1_to_ags_list.setdefault(ad["url"], []).append(temp_ad)
        return url_step1_to_ags_list

    """
    This method divide the items by url
    Complexity = O(n^2)
    :return dictionary with key = url name values = list of (ag_id, ad_id)
    """
    @staticmethod
    def divide_by_url(url_to_ags_list):
        url_step2_to_ags_list = {}
        for url in url_to_ags_list:
            url_step2_to_ags_list[url] = url_to_ags_list[url]
            for url_compare in url_to_ags_list:
                if url_compare != url and urls_are_equal(url_compare, url):
                    url_step2_to_ags_list[url].appand(url_to_ags_list[url])
                    url_to_ags_list.pop(url)
        return url_step2_to_ags_list

    """
    This method divide the items by image
    Complexity = O(n^2)
    :return dictionary with key = url name values = list of (ag_id, ad_id)
    """
    @staticmethod
    def divide_by_image(url_to_ags_list):
        url_step3_to_ags_list = {}
        for url in url_to_ags_list:
            url_step3_to_ags_list[url] = url_to_ags_list[url]
            for url_compare in url_to_ags_list:
                if url_compare != url and images_are_equal(url_compare, url):
                    url_step3_to_ags_list[url].appand(url_to_ags_list[url])
                    url_to_ags_list.pop(url)
        return url_step3_to_ags_list


if __name__ == '__main__':
    AlbertContainer().main()
