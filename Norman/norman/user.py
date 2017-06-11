# from Norman.conversation.norman import norman
from Norman.auth.auth_utils import PatientUtil
from Norman.models import UserModel


class NormanUser(PatientUtil):
    def __init__(self):
        super(NormanUser, self).__init__()
        self.is_from_ref_id = None
        self.instantiated_user = None
        self.session_id = None

    def update_ref_id(self, refID, fb_id):
        return True if UserModel.objects.filter(referenceID=refID).update(fb_id=fb_id, has_hospital=True) else False

    def isRegistered(self, fb_id):
        return True if self.get_by_fbID(fb_id=fb_id) else False
