"""
The API declarations

This is the BentoML class that defines the API and how the are handled.
These APIs use other deep-learning packages we developed in order to
perform these functionalities.

The following are Endpoint currently provided.

    1. Image Captioning: '/captioning'
        Takes an image and returns a string with the generated caption

    2. Object Detection: '/dectection'
        Takes and image and returns a json with the objects, bounding
        boxes and their confidence scores.

    [TODO] 3. Face Detection: '/face'
        Takes an image and checks for matches with any face given in
        the database.

        '/addface'
        Takes an image adds it to the database.
"""

import os

import bentoml
from bentoml.artifact import PytorchModelArtifact
from bentoml.handlers import ImageHandler

from imagecaptioning import ImageCaptioner

@bentoml.env(pip_dependencies=['torch', 'torchvision'])
@bentoml.artifacts([PytorchModelArtifact('imgcap_encoder'),
                    PytorchModelArtifact('imgcap_decoder')])
class AeyeService(bentoml.BentoService):
    """
    The different Services provided

    The AeyeService handles the API requests and passes the data to
    the other modules that we use to perform its deep learning
    functionalities. Each method corresponds to an API end point.
    """

    @bentoml.api(ImageHandler)
    def captioning(self, img):
        """
        The Image Captioning Endpoint

        It first initiates a model using the ImageCaptioner class from
        the imagecaptioning package that is created to handle image
        captioning tasks.

        It loads the model using artifacts provided (wordmap, encoder,
        decoder).

        Parameters
        ----------
        img:
            an 3D array represending the image.

        Returns
        -------
        str
            The caption generated for the image
        """
        print(type(img))

        # using abs path for wordmap
        dir_path = os.path.dirname(os.path.realpath(__file__))
        wordmap = dir_path + '/wordmap.json'

        model = ImageCaptioner(encoder=self.artifacts.imgcap_encoder,
                               decoder=self.artifacts.imgcap_decoder,
                               word_map_file=wordmap)

        sent = model.gen_caption(img)
        return sent
