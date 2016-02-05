# -*- coding: utf-8 -*-
##############################################################################
#
#    pdf report support for your language - OpenERP Module
#    Copyright (C) 2013 Shine IT (<http://www.openerp.cn>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# bug from :http://two.pairlist.net/pipermail/reportlab-users/2012-January/010336.html
# get fonts name and file path
# ff.search() may resulting error if any AFMFont resided in
# the search path has defined width that is not an integer
# a dirty workaround:
# replace following code around #110 in reportlab.pdfbase.pdfmetrics
# From:
# width = string.atoi(r)
# To:
# width = int(float(r))
import string
import reportlab.pdfbase.pdfmetrics 
from reportlab.lib.utils import open_and_readlines

def parseAFMFile(afmFileName):
    """Quick and dirty - gives back a top-level dictionary
    with top-level items, and a 'widths' key containing
    a dictionary of glyph names and widths.  Just enough
    needed for embedding.  A better parser would accept
    options for what data you wwanted, and preserve the
    order."""

    lines = open_and_readlines(afmFileName, 'r')
    if len(lines)<=1:
        #likely to be a MAC file
        if lines: lines = string.split(lines[0],'\r')
        if len(lines)<=1:
            raise ValueError, 'AFM file %s hasn\'t enough data' % afmFileName
    topLevel = {}
    glyphLevel = []

    lines = [l for l in map(string.strip, lines) if not l.lower().startswith('comment')]
    #pass 1 - get the widths
    inMetrics = 0  # os 'TOP', or 'CHARMETRICS'
    for line in lines:
        if line[0:16] == 'StartCharMetrics':
            inMetrics = 1
        elif line[0:14] == 'EndCharMetrics':
            inMetrics = 0
        elif inMetrics:
            chunks = string.split(line, ';')
            chunks = map(string.strip, chunks)
            cidChunk, widthChunk, nameChunk = chunks[0:3]

            # character ID
            l, r = string.split(cidChunk)
            assert l == 'C', 'bad line in font file %s' % line
            cid = string.atoi(r)

            # width
            l, r = string.split(widthChunk)
            assert l == 'WX', 'bad line in font file %s' % line
            #width = string.atoi(r)
            width = int(float(r))

            # name
            l, r = string.split(nameChunk)
            assert l == 'N', 'bad line in font file %s' % line
            name = r

            glyphLevel.append((cid, width, name))

    # pass 2 font info
    inHeader = 0
    for line in lines:
        if line[0:16] == 'StartFontMetrics':
            inHeader = 1
        if line[0:16] == 'StartCharMetrics':
            inHeader = 0
        elif inHeader:
            if line[0:7] == 'Comment': pass
            try:
                left, right = string.split(line,' ',1)
            except:
                raise ValueError, "Header information error in afm %s: line='%s'" % (afmFileName, line)
            try:
                right = string.atoi(right)
            except:
                pass
            topLevel[left] = right


    return (topLevel, glyphLevel)

reportlab.pdfbase.pdfmetrics.parseAFMFile = parseAFMFile

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: