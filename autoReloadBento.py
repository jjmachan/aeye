import sys
import time
import logging
import multiprocessing
from os.path import abspath

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.utils import has_attribute, unicode_paths
from pathtools.patterns import match_any_paths
from bentoml.server import BentoAPIServer

import aeye
from aeye import AeyeService
from imagecaptioning import ImageCaptioner
from objectDetection import InferencingModel


class BentoServiceChangeHandler(FileSystemEventHandler):
    """
    Takes the service module and a server init function that
    handles the events (in this case modification of the service file).

    It spins off a new process for each server and when a change
    is detected it kills it and starts a new server
    """

    def __init__(self, BentoServiceModule, server_init):
        super(BentoServiceChangeHandler, self).__init__()

        self._server_init = server_init
        self._file = BentoServiceModule.__file__
        self._server = multiprocessing.Process(target=self._server_init)
        self._server.start()

        print('Watching %s'%(self._file))
    def on_modified(self):
        print("Modified %s. Restarting server ..."%(self._file))
        self._server.terminate()
        self._server.join()
        self._server = multiprocessing.Process(target=self._server_init)
        self._server.start()

    def dispatch(self, event):
        """
        Dispatches events to the appropriate methods.
        """
        #ahhhh
        if abspath(event.src_path) == self._file and event.event_type == 'modified':
            self.on_modified()
        return



def init_bentoServer():
    """
    Initialize and start the server
    """
    # ImageCaptioning lib
    imgcap_wordmap = 'artifacts/imgcap_wordmap.json'
    imgcap_checkpoint = 'artifacts/imgcap_checkpoint.pth.tar'
    # Obect Detection lib
    objectdetection_checkpoint = 'artifacts/objdet_checkpoint.pth.tar'


    imgcap_model = ImageCaptioner(word_map_file=imgcap_wordmap,
                                  checkpoint=imgcap_checkpoint)
    objdet_model = InferencingModel(checkpoint_file=objectdetection_checkpoint)


    aeye = AeyeService()
    aeye.pack('imgcap_encoder', imgcap_model.encoder)
    aeye.pack('imgcap_decoder', imgcap_model.decoder)
    aeye.pack('objdet_model', objdet_model.model)

    port = 5000
    api_server = BentoAPIServer(aeye, port=port)
    api_server.start()
    print('Server started!')

if __name__ == "__main__":

    my_event_handler = BentoServiceChangeHandler(aeye, init_bentoServer)

    path = "."
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
    my_observer.join()
