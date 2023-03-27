from libs.sec.anti_virus import AntiVirus
from libs.sec.spam_detector import ImageVerifier
from libs.sec.spam_detector import FileSizeVerifier


class SecurityManager(AntiVirus, ImageVerifier, FileSizeVerifier):
    pass
