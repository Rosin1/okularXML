# coding:utf-8
'''
file noted by okular

    1. rename file
        change okular xml

    2. delete file
        delete okular xml

    3. get xml

    4. delete xml

'''
import os
import sys
from glob import glob

import log


class HandleOkularXml:

    def __init__(self, mylog):
        """init."""
        self.mylog = mylog
        self.filename = ""
        self.filename_base = ""
        self.xml_path = "/home/zzp/.kde/share/apps/okular/docdata/"
        self.xmlfilename = ""
        self.id = ""

    def config(self, filename):
        """input filename, set some values and find xml."""
        self.filename = filename
        self.filename_base = os.path.basename(self.filename)
        self.xmlfilename = ""
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
                self.mylog.info(self.xml_path)
                self.mylog.fatal("please handle it youself.")
                sys.exit(1)
            self.xmlfilename = result[0]
            xmlfilename_base = os.path.basename(self.xmlfilename)
            self.mylog.debug("found xml: %s" % self.xmlfilename)
            self.id = xmlfilename_base[:xmlfilename_base.index(".")]
            self.mylog.debug("found id: %s" % self.id)

    def rename(self, newname):
        """rename document and rename xml at the same time"""
        if os.path.dirname(newname) == "":
            self.mylog.warn("newname will be added path by the script.")
            newname = os.path.join(os.path.dirname(self.filename), newname)
        os.rename(self.filename, newname)
        self.mylog.done("doc rename done.")
        self.mylog.debug("xml: %s" % self.xmlfilename)
        if os.path.exists(self.xmlfilename):
            assert os.path.exists(self.xmlfilename)
            newxmlname = os.path.join(self.xml_path,
                                      "%s.%s.xml" % (self.id, os.path.basename(newname)))
            self.mylog.debug("new xml: %s" % newxmlname)
            os.rename(self.xmlfilename, newxmlname)
            self.mylog.done("xml rename done.")

    def delete(self):
        """delete document and xml"""
        os.remove(self.filename)
        self.mylog.done("doc has been deleted.")
        if self.xmlfilename != "":
            os.remove(self.xmlfilename)
            self.mylog.done("xml has been deleted.")

    def getxml(self):
        """get xml to each document dir."""
        import shutil
        if not os.path.exists(self.xmlfilename):
            self.mylog.error("xml not found!")
        else:
            self.mylog.info("xml: %s" %self.xmlfilename)
            shutil.copyfile(self.xmlfilename,
                            os.path.join(os.path.dirname(self.filename),
                                         os.path.basename(self.xmlfilename)))
            self.mylog.done('xml has been copied into document dir.')

    def deletexml(self):
        if not os.path.exists(self.xmlfilename):
            self.mylog.error("xml not found!")
        else:
            os.remove(self.xmlfilename)
            self.mylog.done('xml has been deleted.')


def parse(mylog):
    import argparse
    parser = argparse.ArgumentParser(
        description='handle the xmls of okular reader.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--rename', nargs="*",
                       action='store', help='rename doc.')
    group.add_argument('-d', '--delete', nargs="*",
                       action='store', help='delete doc.')
    group.add_argument('-g', '--getxml', nargs="*",
                       action='store', help='get xml to each document dir.')
    group.add_argument('-dx', '--deletexml', nargs="*",
                  action='store', help='delete xml of each documents.')
    parser.add_argument('-x', '--xml', action='store_true',
                        help='show xml path.')
    args = parser.parse_args()
    return args


def main(mylog, args):
    """main test."""
    if args.xml == True:
        hox = HandleOkularXml(mylog)
        mylog.done(hox.xml_path)
    elif args.delete != None:
        mylog.debug("correct delete args.")
        for filename in args.delete:
            hox = HandleOkularXml(mylog)
            mylog.info('file: %s' % filename)
            hox.config(filename)
            hox.delete()
    elif args.rename != None and len(args.rename) == 2:
        mylog.debug("correct rename args.")
        filename, newname = args.rename
        hox = HandleOkularXml(mylog)
        mylog.info('file: %s' % filename)
        hox.config(filename)
        hox.rename(newname)
    elif args.getxml != None:
        mylog.debug("correct getxml args.")
        for filename in args.getxml:
            hox = HandleOkularXml(mylog)
            mylog.info('file: %s' % filename)
            hox.config(filename)
            hox.getxml()
    elif args.deletexml != None:
        mylog.debug("correct deletexml args.")
        for filename in args.deletexml:
            hox = HandleOkularXml(mylog)
            mylog.info('file: %s' % filename)
            hox.config(filename)
            hox.deletexml()
    else:
        mylog.fatal("wrong args.")
        sys.exit(1)


if __name__ == '__main__':
    # log
    mylog = log.Terminal_log(brief=True)
    args = parse(mylog)
    main(mylog, args)
