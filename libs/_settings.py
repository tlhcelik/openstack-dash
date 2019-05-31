from views import Views
v = Views()

from flask import Flask, flash, redirect, render_template, request, session, abort, Markup

class Settings(object):
    """docstring for Settings."""

    def __init__(self):
        print "Settings init"

    def do_it_some_transaction(self):
        return "i make some transaction. example : return uname -a"
