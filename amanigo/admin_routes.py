from PIL import Image
import json, os
import io
from os.path import basename
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from flask import * 
from flask_socketio import SocketIO, emit, join_room, leave_room
from markupsafe import escape
import re 
from flask_wtf.csrf import CSRFProtect, generate_csrf
from amanigo import *
from amanigo.forms import *
from flask_login import login_required
from amanigo.models import db
from sqlalchemy import func,desc  
from datetime import datetime
