import json
import numpy as np


class MisleadingAds(object):
    CTR_FACTOR = 1.5
    CR_FACTOR = 1.5
    MIN_IMPS = 10
    MIN_ITEMS = 5
    FILE = 'ads.json'
    ads = {}

    def main(self):
        # create the ads list from the json file
        with open(self.FILE) as json_file:
            self.ads = json.load(json_file)
        ag_to_stats = self.get_ags_stats()
        ag_to_calculated_parameters = self.calculate_ags_measures(ag_to_stats)
        misleading_ads = self.find_misleading_ads(ag_to_calculated_parameters)
        print(misleading_ads)

    """
    This method insert the ctr, cr, items, imps from each ad into the relevant ag
    Complexity = O(n)
    :return dictionary with key = ag_id values = ctr list, cr list, items counter and num of imps
    """

    def get_ags_stats(self):
        ag_to_stats = {}
        for ad in self.ads:
            if ad["clicks"] > 0:
                ag_to_stats.setdefault(ad["ad_group_id"], {}).setdefault("ctr", []).append(
                    (ad["clicks"] / ad["impressions"]))
                ag_to_stats.setdefault(ad["ad_group_id"], {}).setdefault("cr", []).append(
                    ad["conversions"] / ad["clicks"])
                ag_to_stats.setdefault(ad["ad_group_id"], {}).setdefault("imps", []).append(ad["impressions"])
        return ag_to_stats

    """
    This method calculate the avg_ctr, avg_cr, std_ctr, std_cr for each ag
    Complexity = O(m) [m - num of ags]
    :return dictionary with key = ag_id values = avg_ctr, avg_cr, std_ctr, std_cr
    """

    def calculate_ags_measures(self, ag_to_stats):
        ag_to_final_ctr_cr = {}
        for ag_id, ag in ag_to_stats.items():
            if len(ag["imps"]) > self.MIN_ITEMS and sum(ag["imps"]) > self.MIN_IMPS:
                ag_to_final_ctr_cr[ag_id] = {"avg_ctr": np.average(ag["ctr"]),
                                             "avg_cr": np.average(ag["cr"]),
                                             "stdev_ctr": np.std(ag["ctr"]),
                                             "stdev_cr": np.std(ag["cr"]),
                                             }
        return ag_to_final_ctr_cr

    """
    This method find the misleading ads
    Complexity = O(n)
    :return list of tuples of the misleading ads
    """

    def find_misleading_ads(self, ag_to_calculated_parameters):
        misleading_ads = []
        for ad in self.ads:
            ctr_threshold = ag_to_calculated_parameters[ad["ad_group_id"]]["avg_ctr"] + \
                            self.CTR_FACTOR * ag_to_calculated_parameters[ad["ad_group_id"]]["stdev_ctr"]
            cr_threshold = ag_to_calculated_parameters[ad["ad_group_id"]]["avg_cr"] - \
                           self.CR_FACTOR * ag_to_calculated_parameters[ad["ad_group_id"]]["stdev_cr"]
            if ad["clicks"] > 0:
                ad_ctr = ad["clicks"] / ad["impressions"]
                ad_cr = ad["conversions"] / ad["clicks"]
                if ad_ctr > ctr_threshold and ad_cr < cr_threshold:
                    misleading_ads.append((ad["ad_group_id"], ad["ad_id"]))
        return misleading_ads


if __name__ == '__main__':
    MisleadingAds().main()
