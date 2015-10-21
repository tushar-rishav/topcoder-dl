from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from setproctitle import setproctitle
import os
import urllib2
import subprocess
import argparse
import sys

__author__ = 'tushar-rishav'
__version__ = "0.0.2"


class TopCoder:

    def __init__(self):
        self.base_url = "https://www.topcoder.com/community/data-science/data-science-tutorials/"
        self.target_dir = "TopcoderPdf"
        self.flag = False
        setproctitle('topcoderdl')

    def fetch(self):
        try:
            if not os.path.exists(self.target_dir):
                os.mkdir(self.target_dir)
        except Exception as e:
            print(e)
        self.page = urllib2.urlopen(self.base_url)
        self.data = BeautifulSoup(self.page.read(), "lxml")
        if not self.flag:
            table = self.data.findAll("table")[0]
            all_a = table.findAll("a")
            member_a = table.findAll("a", class_="tc_coder coder")
            all_set = set(all_a)
            member_set = set(member_a)
            post = list(set(all_set).difference(member_set))
        else:
            post = [self.base_url]

        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_url = {
                executor.submit(self.download, url): url for url in post}
            for future in as_completed(future_to_url):
                url = future_to_url[future]

    def download(self, url):

        if not self.flag:
            post_name = os.path.join(self.target_dir, url.get_text())
            post_url = url['href']
        else:
            post_name = os.path.join(
                self.target_dir, self.data.title.getText())
            post_url = url
        print("Downloading " + post_name + "....")
        args = ['wkhtmltopdf', post_url, post_name+".pdf"]
        subprocess.Popen(args)


class Smarty(TopCoder):

    def __init__(self, _):
        pass

    def __call__(self, func):
        def read(obj):
            args = func()
            if args.target:
                obj.target_dir = args.target
            if args.post:
                obj.base_url = args.post
                obj.flag = True

        return read


@Smarty(None)
def parse():
    parser = argparse.ArgumentParser(description=" \
             Downloads Topcoder algorithm tutorials and save as PDF", epilog="\
             Author:https://github.com/tushar-rishav")
    parser.add_argument("-t", "--target", help="absolute path of target directory to save all PDFs. Default is TopcoderPdf in current dir",
                        type=str)
    parser.add_argument("-p", "--post", help="link for single post",
                        type=str)
    args = parser.parse_args()
    return args


def main():

    obj = TopCoder()
    parse(obj)
    obj.fetch()

if __name__ == "__main__":
    main()
