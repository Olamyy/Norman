import datetime
from bson import ObjectId
from Norman.auth.auth_utils import PatientUtil, ServiceUtil, HospitalUtil
from Norman.models import Conversation, Notification
from googleplaces import GooglePlaces, types, lang
from Norman.settings import GoogleConfig
import googlemaps

class RealTimeMessagingService:
    def __init__(self, fb_id,message,**kwargs):
        self.fb_id = fb_id
        self.user = PatientUtil().get_by_fbID(fb_id)
        self.message = message
        self.intent_trigger = kwargs.get('IntentTrigger', None)
        self.is_new = kwargs.get('is_new', None)
        self.missing = kwargs.get('missing', None)
        self.context = kwargs.get('context', None)
        self.person = kwargs.get('recipient', None)

    def getResponse(self):
        if self.user.has_hospital:
            if self.is_new:
                conversation_object = Conversation(fb_id=self.fb_id, created_at=datetime.datetime.now(), is_alive=True,
                                                        service='messaging')
                if not self.intent_trigger:
                        notification = Notification(sender_id=self.fb_id,
                                                    created_at=datetime.datetime.now(),
                                                    is_read = False,
                                                    message = self.message)
                        #@Todo: Also send email to hospital about the notification
                        return {'status':'success', 'response':'message_success'}
                else:
                        Conversation.objects(id=ObjectId(conversation_object.id),
                                             fb_id=self.fb_id).update(missing=self.missing, is_complete=False)
                        response = {'status': 'pending', 'response':'incomplete_intent'}
                        return response
            else:
                if self.intent_trigger:
                    Conversation.objects(fb_id=self.fb_id, is_complete=False, service='messaging').update(missing=self.missing)
                    response = {'status': 'pending', 'response': 'incomplete_intent'}
                    return response
        else:
            response = {'status': 'error', 'err_ID': 'NoRegisteredHosp'}
            return response


class LocationService:
    def __init__(self, fb_id, message,**kwargs):
        self.fb_id = fb_id
        self.user = PatientUtil().get_by_fbID(fb_id)
        self.message = message
        self.intent_trigger = kwargs.get('IntentTrigger', None)
        self.is_new = kwargs.get('is_new', None)
        self.missing = kwargs.get('missing', None)
        self.context = kwargs.get('context', None)
        self.go_to = kwargs.get('go_to')
        self.gmaps = googlemaps.Client(GoogleConfig.PLACES_API_KEY)

    def getResponse(self):
        if self.user.has_hospital:
            if self.is_new:
                conversation_object = Conversation(fb_id=self.fb_id, created_at=datetime.datetime.now(), is_alive=True,
                                                        service='location')
                if not self.intent_trigger:
                    if self.message == 'self_location_finder':
                        Conversation.objects(fb_id=self.fb_id, service='location', id=ObjectId(conversation_object.id)).update(is_expecting='lat_long')
                        return 'request_location'
                    elif self.message == 'self_hospital_finder':
                        return 'request_location'
                    elif self.message == 'nearest_hospital_finder':
                        return 'request_location'
                    elif self.message in ['nearest_pharmarcy' , 'nearest_drugstore']:
                        return 'request_location'
                else:
                    if self.message == 'self_location_finder':
                        Conversation.objects(fb_id=self.fb_id, is_complete=False, service='location', is_alive=True).update(
                            missing=self.missing)
                        response = {'status': 'pending', 'response': 'incomplete_intent'}
                        return response
            else:
                if not self.intent_trigger:
                    lat_lang = {'lat': self.message.get('lat'), 'lng': self.message.get('lng')}
                    if self.message == 'self_location_finder' :
                        if self.context == 'lat_long':
                            place_search = self.getCurrentLocation(lat_lng=lat_lang)
                            response = {'status': 'success', 'response': place_search}
                    elif self.message == 'self_hospital_finder':
                        if self.context == 'direction':
                            direction = self.getDirection(lat_lang, self.go_to)
                        if self.context == 'address':
                            hospital_id = self.user.hospital_id
                            get_address = HospitalUtil().get_by_id(ObjectId(hospital_id))
                            if get_address:
                                response = {'status':'success', 'response':get_address.address}
                                return response
                            else:
                                response = {'status': 'error', 'err_ID':'NoRegisteredHosp'}
                                return response
                    elif self.message == 'nearest_hospital_finder':
                        pass
        else:
            response = {'status': 'error', 'err_ID': 'NoRegisteredHosp'}
            return response


    def getCurrentLocation(self, lat_lng):
        reverse_geocode_result = self.gmaps.reverse_geocode((lat_lng[0], lat_lng[1]))
        return reverse_geocode_result[2]['formatted_address']

    def searchCurrentLocation(self, lat_lng, place):
        return

    def getDirection(self, start_from, go_to):
        routes = self.gmaps.directions(start_from, go_to,
                                       mode="transit",
                                       traffic_model="optimistic",
                                       departure_time=datetime.datetime.now())






