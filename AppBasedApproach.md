# Introduction #

Rather than do all this integration up front ... do it later.

# Details #

So first build the standalone tools i.e. web services
  1. grid based page layout editor
  1. javascript + media components
  1. django modules: story/media/promos

Break everything up into separate projects.  Django newsroom will have a stake in all those projects but each project will live on its own and anyone can use it/contribute.

Asking people to contribute to DN is heavy ... asking them to use/integrate our standalone stuff is light.

These disparate projects could be brought in via requirements/external\_apps.txt that is, if it's python.

If not, (in the case of the app being just be html + javascript) we just fork it. Or integrate it if possible without forking, similar to jquery-ui