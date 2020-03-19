# -*- coding: utf8 -*-
from flask import Blueprint

# 这个名字指向app下的init
home = Blueprint("home", __name__)

import app.home.views
