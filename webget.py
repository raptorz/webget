# -*- coding: UTF-8 -*-
#!/usr/local/bin/python

# 通过wget下载文件，提供web管理界面
# author : raptor.zh@gmail.com
# create : 2015/03/18
#          2015/08/10
from __future__ import unicode_literals
import sys
PY3=sys.version>"3"

import os
from os.path import getsize, join as joinpath

import requests

from bottle import Bottle, run, request, response, redirect, static_file, mako_view as view
from subprocess import Popen
from shlex import split as cmd_split

from params_plugin import ParamsPlugin
from config import config, get_fullname

import logging

logger = logging.getLogger(__name__)


app = Bottle()
app.install(ParamsPlugin())


# dict: pid, filename, url, size, proc
jobdata = []


def get_status(job):
    try:
        filename = joinpath(config["down_dir"], job["filename"])
        prog = 0 if job["size"]==0 else int(getsize(filename) * 100.0 / job["size"] + 0.5)
    except os.error:
        prog = 0
    status = "Doing"
    proc = job["proc"]
    if proc:
        proc.poll()
        if proc.returncode == 0:
            status = "Done"
        elif proc.returncode != None:
            status = "Job fail code: %s" % proc.returncode
    else:
        status = "Canceled"
    return (status, prog)


def subproc_job(filename, url):
#    filename = joinpath(config["down_dir"], filename)
    cmd = "%s -q -c -O %s \"%s\"" % (joinpath(config["wget_dir"], "wget"), filename, url)
    logger.debug(cmd)
    p = Popen(cmd_split(cmd), cwd=config["down_dir"], shell=False)
    return p


def joblist(jobdata):
    def jobstatus(job):
        ret={}
        [ret.__setitem__(k,v) for k,v in job.items() if k!="proc"]
        ret["status"], ret["progress"] = get_status(job)
        return ret
    return [jobstatus(job) for job in jobdata]


def findfile(filename):
    for job in jobdata:
        if job["filename"]==filename:
            return job
    return None


def killjob(job):
    proc = job['proc']
    if proc:
        proc.poll()
        if proc.returncode == None:
            proc.terminate()
    job['proc'] = None


def findpid(pid):
    for job in jobdata:
        if job["pid"]==pid:
            return job
    return None


def deljob(job):
    filename = joinpath(config["down_dir"], job["filename"])
    os.remove(filename)
    del jobdata[jobdata.index(job)]


def resumejob(job):
    proc = subproc_job(job["filename"], job["url"])
    job["proc"] = proc
    job["pid"] = proc.pid


@app.get("/static/<filename:path>")
def get_static(filename):
    return static_file(filename, root=get_fullname("static"))


@app.get("/")
@view("index.html")
def get_index():
    return dict(joblist=joblist(jobdata), base=config['web_path'], web_down=config['web_down'])


@app.post("/")
def post_index(url, filename):
    url = url.strip()
    filename = filename.strip()
    if filename and url:
        job = findfile(filename)
        if not job:
            resp = requests.head(url)
            try:
                size = int(resp.headers["content-length"])
                proc = subproc_job(filename, url)
                job = dict(pid=proc.pid, filename=filename, url=url, size=size, proc=proc)
                jobdata.insert(0, job)
            except KeyError:
                pass
    redirect("/%s" % config["web_path"])


@app.post("/<pid:int>")
def post_job(pid, action):
    job = findpid(pid)
    if job:
        if action=="delete":
            deljob(job)
        elif action=="cancel":
            killjob(job)
        else:
            resumejob(job)
    redirect("/%s" % config["web_path"])


application = Bottle()

application.mount("/%s" % config["web_path"], app)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG if config['debug'] else logging.WARNING)
    run(application, host=config['web_addr'], port=config['web_port'], debug=config['debug'], reloader=config['debug'])
