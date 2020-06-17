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
import json

import numpy as np
from PIL import Image
import bentoml
from bentoml.artifact import PytorchModelArtifact, PickleArtifact
from bentoml.handlers import ImageHandler

from imagecaptioning import ImageCaptioner
from objectDetection import InferencingModel
from facedetection import FaceDetection

@bentoml.env(pip_dependencies=['torch', 'torchvision'])
@bentoml.artifacts([PytorchModelArtifact('imgcap_encoder'),
                    PytorchModelArtifact('imgcap_decoder'),
                    PytorchModelArtifact('objdet_model'),
                    PytorchModelArtifact('mtcnn'),
                    PytorchModelArtifact('inception_net'),
                    PickleArtifact('db')])
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
    @bentoml.api(ImageHandler)
    def detection(self, img):
        """
        The finale test
        """
        img = np.asarray(img)
        img = Image.fromarray(img)
        print(type(img))

        model = InferencingModel(artifact=self.artifacts.objdet_model)

        labels, boxes = model(img, min_score=0.2, top_k=200, max_overlap=0.5)
        print(labels)

        json_obj = dict()
        output = list()
        for i in range(len(labels)):
            json_obj[i] = [labels[i], boxes[i].tolist()]
            output.append(json_obj)

        print(output)
        output_json = json.dumps(output)
        print(output_json)
        return output_json

    @bentoml.api(ImageHandler)
    def face_recognition(self, img):
        """ takes an image and recognises if it is the database

        """
        img = np.asarray(img)
        img = Image.fromarray(img)

        facedetect = FaceDetection(mtcnn=self.artifacts.mtcnn,
                                   inception_net=self.artifacts.inception_net,
                                   db=self.artifacts.db)
        name, prob = facedetect.recognise_face(img)
        return name,prob

