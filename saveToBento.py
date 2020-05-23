"""
Script to pack the models to be served via BentoML

This script loads and Intialises the various models used to perform
the services. Then the models are packed and saved to disk. Any of the
artifacts that are not supported are packed using this script
"""
import shutil

from imagecaptioning import ImageCaptioner
from aeye import AeyeService

##########
# CONFIG
##########

# ImageCaptioning lib
imgcap_wordmap = 'artifacts/imgcap_wordmap.json'
imgcap_checkpoint = 'artifacts/imgcap_checkpoint.pth.tar'




##########
# INIT
##########

imgcap_model = ImageCaptioner(word_map_file=imgcap_wordmap,
                              checkpoint=imgcap_checkpoint)


##########
# PACK
##########

aeye = AeyeService()
aeye.pack('imgcap_encoder', imgcap_model.encoder)
aeye.pack('imgcap_decoder', imgcap_model.decoder)



########
# SAVE
########

saved_file = aeye.save()
dest = saved_file + '/AeyeService/wordmap.json'
shutil.copy(imgcap_wordmap, dest)
