# coding:utf-8
'''
file noted by okular

    1. rename file
        change okular xml

    2. delete file
        delete okular xml

list all xmls(ignore that is needed)
    delete useless.
'''
import os
import sys
from glob import glob

import log


class HandleOkularXml():

    def __init__(self, mylog):
        """init."""
        self.mylog = mylog
        self.filename = ""
        self.filename_base = ""
        self.xml_path = ""
        self.xml_important = ""
        self.xmlfilename = ""
        self.xmlfilename_base = ""
        self.id = ""

    def config(self, filename):
        """input filename, set some values and find xml."""
        self.filename = filename
        self.filename_base = os.path.basename(self.filename)
        self.xml_path = "/home/zzp/.kde/share/apps/okular/docdata/"
        self.xml_important = os.path.join(self.xml_path, "important.txt")
        self.xmlfilename = ""
        self.xmlfilename_base = ""
        self.id = ""
        if not os.path.exists(self.filename):
            self.mylog.fatal('%s cannot be found!' % self.filename)
            sys.exit(1)
        self.get_xmlfilename()

    def get_xmlfilename(self):
        assert os.path.exists(self.filename)
        result = glob(os.path.join(
            self.xml_path, "*" + self.filename_base + ".xml"))
        if result == []:
            self.xmlfilename = ""
        else:
            if len(result) != 1:
                self.mylog.error("found more than one xml:\n%s" % result)
                sys.exit(1)
            self.xmlfilename = result[0]
            self.xmlfilename_base = os.path.basename(self.xmlfilename)
            self.mylog.debug("found xml: %s" % self.xmlfilename)
            self.id = self.xmlfilename_base[:self.xmlfilename_base.index(".")]
            self.mylog.debug("found id: %s" % self.id)
            pass

    def rename(self, newname):
        """rename document and rename xml at the same time"""
        if os.path.dirname(newname) == "":
            self.mylog.warn("newname will be added path by the script.")
            newname = os.path.join(os.path.dirname(self.filename), newname)
            os.rename(self.filename, newname)
            self.mylog.debug("xml: %s" % self.xmlfilename)
            if os.path.exists(self.xmlfilename):
                assert os.path.exists(self.xmlfilename)
                newxmlname = os.path.join(self.xml_path,
                                          "%s.%s.xml" % (self.id, os.path.basename(newname)))
                self.mylog.debug("new xml: %s" % newxmlname)
                os.rename(self.xmlfilename, newxmlname)

    def delete(self):
        """delete document and xml"""
        os.remove(self.filename)
        self.mylog.info("%s has been deleted." % self.filename)
        if self.xmlfilename != "":
            os.remove(self.xmlfilename)
            self.mylog.info("%s has been deleted." % self.xmlfilename)


def main():
    """main test."""
    mylog = log.Terminal_log(brief=False)
    hox = HandleOkularXml(mylog)

    mylog.info("input filename:")
    filename = "/home/zzp/test_back.pdf"  # raw_input()
    mylog.info('file: %s' % filename)
    hox.config(filename)

if __name__ == '__main__':
    main()
