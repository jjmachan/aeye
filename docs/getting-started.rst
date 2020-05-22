Getting started
===============

**Note:** *The most reliable way to use this service is to host it on your own
local machine. It does not take huge resources and standard cpu with 4gigs or
ram is adequate. Aeye does provide an online service but it is hosted on a trial
account in GCP and we don't know how often we can afford to run it.*

Using the Online Service 
------------------------

This is the easiest way to use the API. It accepts simple POST requests with the
images and returns the corresponding responses in json format. Lets jump right
in and test out the Image Captioning service.

The following curl request should generate the captions for the image ::
   
   #TODO: host it
   curl POST https://aeye-service.herokuapp.com/captioning -H "Content-Type:
   image/*" --data-binary @YOUR-IMG.jpg -v

This will set a POST request to the service and will return a string with the
caption that the model generated.

If you want to use it in a program, we recommend that you use libraries like
``requests`` for handling http requests to the service. ::

   import requests

   #TODO: Remaining

Offline Serving 
---------------

You can also run the Aeye service in your local environment using `BentoML
<https://docs.bentoml.org/en/latest/>`_. BentoML is used to pack and save the
models that we use. Since the serving is based on BentoML I suggest you check it
out to get a better idea about the library.

First git clone this repo to your local environment and install all the
requirments. ::

   $ git clone https://github.com/jjmachan/aeye 
   $ cd aeye 
   $ pip install -r requirements.text

Now you have all the dependencies setup. The next step is to download all the
artifacts and put it in the artifacts page. Files like the trained weights for
the models, the wordmap used are all downloaded from the appropriate links given
bellow and all of them are to be placed in the `artifacts/` directory.

* Image Captioning: 

  * Encoder - https://localhost
  
  * Decoder - https://localhost

  * WordMap - https://localhost

* Object Dection:

* Facial Recognition

With all of the artifacts downloaded we are now ready to pack the models and
create the containerized version that can be hosted. Now BentoML is handling all
of the hard work for us and all we have to do is run a couple of commands.

First lets save and back the model to a Bento repository. ::

   $ python saveToBento.py

This will save the models, artifacts and pack all of it with the dependencies
into a deployable containerized package. Now use BentoML to serve it. ::

   $ bentoml serve AeyeService:latest

This launches a development server and you can head over to `localhost:5000` to
access the built in API tester. 

Now since we have the service up and running in your local environment all the
steps for using the online service can be carried over. You can use curl or
requests to sent HTTP requests to the APIs.

Now you set to build your stuff using our platform!
