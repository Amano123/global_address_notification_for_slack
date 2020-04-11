#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from multiprocessing import Pool
from cron.cron import JobController

import subprocess
import requests
import time
from variable import kirin

# 別ファイルに記述すること
token      = kirin.token
channel_id = kirin.channel_id
username   = kirin .username


@JobController.run("* * * * *")
def global_add():
    text = subprocess.check_output(["curl ipecho.net/plain"], shell = True)

    # url (post & del)
    post_message_url = 'https://slack.com/api/chat.postMessage'
    del_message_url  = "https://slack.com/api/chat.delete"

    #post 
    post_response = requests.post(post_message_url, data={'token': token,
                                                          'channel':channel_id,
                                                          'text':text,
                                                          'username':username})

    # log 
    logging.info(post_response.json())
    logging.info(text)
    logging.info("post message")
    
    # time sleep
    # もっといい処理があると思う
    time.sleep(6)
    ts = post_response.json()['message']['ts']
    
    # del
    del_response = requests.post(del_message_url, data={'token': token,
                                                        'channel':channel_id,
                                                        'ts':ts})
    # log
    logging.info(del_response)
    logging.info("del message")


def main():
    # ログ設定(Infoレベル、フォーマット、タイムスタンプ)
    logging.basicConfig(
        level=logging.INFO,
        format="time:%(asctime)s.%(msecs)03d\tprocess:%(process)d" + "\tmessage:%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    # crontabで実行したいジョブを登録
    jobs = [global_add]

    # multi process running
    p = Pool(len(jobs))
    try:
        for job in jobs:
            p.apply_async(job)
        p.close()
        p.join()
    except KeyboardInterrupt:
        logging.info("exit")


if __name__ == '__main__':
    main()
