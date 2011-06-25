import bottlenose
from config import amazonconfig

amazon = bottlenose.Amazon(amazonconfig['access_key'], amazonconfig['secret_key'], amazonconfig['tag'], Region=amazonconfig['region'])
