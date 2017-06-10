from textblob import TextBlob
import nltk
import os
import pickle
from textblob.classifiers import NaiveBayesClassifier

nltk.data.path.append(os.path.join(os.getcwd(), "nltk_data"))


class Processor:
    """ Accepts a text message from the bot, triggers appropriate service(s) and sends a properly formated reply
Calls the service class passing the ff args: fb_id, service, service_subtype(if any), fufilment_status
called by the main bot class, accepts fb_id and accompaning text
"""

    def __init__(self, sentence):
        self.sentence = sentence

        classifiers = self.load_trained_classifiers()

        if None in classifiers:
            self.msg_clf, self.loc_clf = classifiers

            if not self.msg_clf:
                self.train_message_classifier()

            if not self.loc_clf:
                self.train_location_classifier()  # train data

        else:
            self.msg_clf, self.loc_clf = classifiers

    def train_message_classifier(self):
        # load train data
        with open('msg_data.json', 'r') as fp:
            self.msg_clf = NaiveBayesClassifier(fp, format="json")  # instantiate classifier
        pickle.dump(self.msg_clf, open("msg.p", "wb"))

    def train_location_classifier(self):
        # load train data
        with open('loc_data.json', 'r') as fp:
            self.loc_clf = NaiveBayesClassifier(fp, format="json")  # instantiate classifier
        pickle.dump(self.loc_clf, open("loc.p", "wb"))

    def load_trained_classifiers(self):
        try:
            msg_clf = pickle.load(open("msg.p", "rb"))
        except FileNotFoundError:
            msg_clf = None
        try:
            loc_clf = pickle.load(open("loc.p", "rb"))
        except FileNotFoundError:
            loc_clf = None
        # loc_clf = pickle.dump(msg_clf)
        return msg_clf, loc_clf

    def classify_sentence(self):
        """ Returns the service"""
        # loc_nearest_hosp, loc_self, loc_pharmacy, loc_my_hosp

        # get probability hint for each service type
        msg_prob = round(self.msg_clf.prob_classify(self.sentence).prob("pos"), 2)
        loc_nearest_hosp_prob = round(self.loc_clf.prob_classify(self.sentence).prob("loc_nearest_hosp"), 2)
        loc_self_prob = round(self.loc_clf.prob_classify(self.sentence).prob("loc_self"), 2)
        loc_pharmacy_prob = round(self.loc_clf.prob_classify(self.sentence).prob("loc_pharmacy"), 2)
        loc_my_hosp_prob = round(self.loc_clf.prob_classify(self.sentence).prob("loc_my_hosp"), 2)

        # get the total probability that the message was for a location service
        # loc_prob = loc_nearest_hosp_prob * loc_self_prob * loc_pharmacy_prob * loc_my_hosp_prob

        # figure out which location service it was
        loc_subtypes_prob = {
            loc_pharmacy_prob: "nearest_pharmacy",
            loc_self_prob: "self_location_finder",
            loc_nearest_hosp_prob: "nearest_hospital_finder",
            loc_my_hosp_prob: "self_hospital_finder"
            }

        print(loc_subtypes_prob)
        loc_prob = max(loc_subtypes_prob.keys())

        loc_subtype = loc_subtypes_prob[max(loc_subtypes_prob.keys())]

        # pick most probable service
        result = {
                    msg_prob: {"name": "messaging_service", "sub_type": "messaging_service"},
                    loc_prob: {"name": "location_service", "sub_type": loc_subtype}
                }
        print(result)
        service = result[max(result.keys())]

        return service

        #### test for multilabel support - sucessful
        # msg_prob =  self.msg_clf.prob_classify(self.sentence).max()
        # loc_prob = self.loc_clf.prob_classify(self.sentence).max()
        # result = {msg_prob: "messaging_service", loc_prob: "location_service"}
        # return result
        ### todo
        # add sub-tags to data samples
        # sub-tags include: 'complete', 'incomplete', 'about_self', etc

    def extract_messaging_details(self):
        msg_blob = TextBlob(self.sentence)
        try:
            receiver = msg_blob.noun_phrases[0]
        except IndexError:
            receiver = None
        # print(receiver)
        return receiver

    def extract_location_details(self):
        return "Coming soon"

    def call_service(self, service):
        print("service received: ", service)
        ### todo
        # check if the user really doesn't have any existing messages on the service

        # IntentTrigger
        # ', None)
        # self.is_new = kwargs.get('is_new', None)
        # self.missing = kwargs.get('missing', None)
        # self.context = kwargs.get('context', None)
        # self.person = kwargs.get('recipient

        data = {
            "IntentTrigger": False,
            "missing": None,
            "is_new": True
        }

        if service["name"] == "messaging_service":
            if not self.extract_messaging_details():
                data["IntentTrigger"] = True
                data["missing"] = "recipient"
            data["recipient"] = self.extract_messaging_details()
            data["text"] = self.sentence

        elif service["name"] == "location_service":
            data["log_lat"] = self.extract_location_details()
            data["IntentTrigger"] = True
            data["missing"] = "log_lat"
            data["service_subtype"] = service["sub_type"]
            if "direction" in self.sentence.lower():
                data["context"] = "direction"
            elif "address" or "addrs" in self.sentence.lower():
                data["context"] = "address"
            else:
                data["context"] = None

        print(data)
        # call appropriate service


if __name__ == '__main__':
    # test = Processor(sentence="message Dr Norman that i will be late")
    test = Processor(sentence="tell me a joke")
    test.call_service(test.classify_sentence())
