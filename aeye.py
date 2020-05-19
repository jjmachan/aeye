import os

import bentoml
from bentoml.artifact import PytorchModelArtifact
from bentoml.handlers import ImageHandler

from imagecaptioning import ImageCaptioner

@bentoml.env(pip_dependencies=['torch', 'torchvision'])
@bentoml.artifacts([PytorchModelArtifact('imgcap_encoder'),
                    PytorchModelArtifact('imgcap_decoder')])
class AeyeService(bentoml.BentoService):

    @bentoml.api(ImageHandler)
    def captioning(self, img):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        wordmap = dir_path + '/wordmap.json'

        model = ImageCaptioner(encoder=self.artifacts.imgcap_encoder,
                               decoder=self.artifacts.imgcap_decoder,
                               word_map_file=wordmap)

        sent = model.gen_caption(img)
        return sent
