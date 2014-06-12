=========================
  Fedora College
=========================

This works to create a virtual classroom for new fedora contributors. Acts as a platform for new contributors to engage with the community and learn how they can contribute best in the community. Mostly this service will be used to run online courses on contributing at various levels be it documentation, bug-fixing or packaging. The project would certainly increase the activeness in the community and certainly make it easy for newer members to craft their way around the fedora community. The use of virtual classroom environment for training new contributors to the community using know educational resources by a combination of written, images and video content.

Fedora College API
------------


|    Endpoint    |                             Feature                           |                               Description                                                              |
|----------------|---------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| /api           | Home page , documentation                                     |  General api documentation and usage                                                                   |
| /api/user/     | User profile, list users, get user by ID, name or email.      |  Get Information about the user and ability to edit and delete profiles. According to privilege level. |
| /api/media/    | media information, get media by ID, version , date , tags     |  Get information about the media content and publish revisions, edit information and delete media.     |
| /api/content/  | content information, get content by ID, version , date , tags |  Get information about the content and publish revisions, edit information and delete content.         |
| /api/comments/ | Get a thread, edits, add more, delete.                        |  Manage Comment stream                                                                                 |
| /api/search    | by Tags , by author , media / content ID                      |  Offer an abstraction for easy searching.                                                              |
| /api/tags      | Add / remove tags                                             |  Manage tags.                                                                                          |
 

Run
------------

1. Create a directory "uploads" , in the static folder.
2. Install oggvideotools (Not a python dependency)
2. python fedora_college/main.py run

Build Status
------------


| Branch   | Status    |
|----------|-----------|
| master   | [![Build Status - master branch](https://secure.travis-ci.org/echevemaster/fedora-college.png?branch=master "Master Branch")](http://travis-ci.org/#!/echevemaster/fedora-college)|
| Develop  | [![Build Status - develop branch](https://secure.travis-ci.org/echevemaster/fedora-college.png?branch=develop "develop Branch")](http://travis-ci.org/#!/echevemaster/fedora-college)|
