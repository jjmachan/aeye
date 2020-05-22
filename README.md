# A-eye

<p align="center">
  <img width="500" height="500" src="https://github.com/jjmachan/aeye/blob/master/docs/imgs/poster.png">
</p>

Aeye aspires to be an open-source AI-as-a-Service platform for hobbyists and
tinkerers to develops apps and services for the visually challenged. We want to
provide the best tools and services for you to go out there and build cool stuff
for our less privileged brothers and sisters, to empower them to prevail over
their shortcomings so that they too can come forth and contribute and fully be a
part of our society. 

The latest advancements in Computer vision thanks to technologies like Deep
Learning we are now able to augment human vision with computer vision models
that help detect the objects around us, detect faces and identify who they are,
describe the environment you are in and much more. This can be of great use to
visually challenged people, to help them perform their day to day tasks more
efficiently. 

The service offers simple to use API end points that help deliver basic deep
learning modules like Object Detection and Image Captioning.

## Modules

Currently we have the following modules planned. Each module is an individual
Python module that is has functionality to perform at least inferencing when
provided with the pretrained models and other artifacts. These modules are
imported into Aeye and the necessary endpoints are created.

The module we support are:

1. [Image Captioning](https://github.com/jjmachan/imagecaptioning-aeye) - This generates a description of the image that is passed
   to it. The current implementation is based on the [Show and
   Tell](https://arxiv.org/abs/1411.4555) paper. This can be used to generate a
   description of the surrounding and is able to give some idea to the user
   about his/her surroundings. Please refer the Module Repo or the docs for more
   information.

2. Object Detection *(still developing)* - This generates the bounding boxes for a range of objects
   and is based on the [Single Shot MuiltiBox
   Detector](https://arxiv.org/abs/1512.02325). 

3. Facial Recognition *(still developing)* - Helps detect faces and identify people around. Also has
   functionality to manage peoples faces for specific users and add new faces to
   the database. 
## Usage

## Contributing

## Sponsorship

We would like to thank [Future Technologies
Lab](https://futuretechnologieslab.com/) under
[KSUM](https://startupmission.kerala.gov.in/) for providing us with the GPU to
build the prototype. 



--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
