"""
Script to pack the models to be served via BentoML

This script loads and Intialises the various models used to perform
the services. Then the models are packed and saved to disk. Any of the
artifacts that are not supported are packed using this script
"""
import shutil

from imagecaptioning import ImageCaptioner
from objectDetection import InferencingModel
from aeye import AeyeService

##########
# CONFIG
##########

# ImageCaptioning lib
imgcap_wordmap = 'artifacts/imgcap_wordmap.json'
imgcap_checkpoint = 'artifacts/imgcap_checkpoint.pth.tar'
objectdetection_checkpoint = 'artifacts/objdet_checkpoint.pth.tar'



##########
# INIT
##########

imgcap_model = ImageCaptioner(word_map_file=imgcap_wordmap,
                              checkpoint=imgcap_checkpoint)
objdet_model = InferencingModel(checkpoint_file=objectdetection_checkpoint)

##########
# PACK
##########

aeye = AeyeService()
aeye.pack('imgcap_encoder', imgcap_model.encoder)
aeye.pack('imgcap_decoder', imgcap_model.decoder)
aeye.pack('objdet_model', objdet_model.model)



########
# SAVE
########

saved_file = aeye.save()
dest = saved_file + '/AeyeService/wordmap.json'
shutil.copy(imgcap_wordmap, dest)
