#
#  content.py
#
#    Parse comment blocks to build content blocks (library file).
#
#  Copyright 2002-2018 by
#  David Turner.
#
#  This file is part of the FreeType project, and may only be used,
#  modified, and distributed under the terms of the FreeType project
#  license, LICENSE.TXT.  By continuing to use, modify, or distribute
#  this file you indicate that you have read the license and
#  understand and accept it fully.

"""This module contains routines to parse documentation comment blocks,
building more structured objects out of them."""

from __future__ import print_function

import logging
import re

from docwriter import sources
from docwriter import utils

log = logging.getLogger( __name__ )

#
# Regular expressions to detect code sequences.  `Code sequences' are simply
# code fragments embedded in '```' and '```', as demonstrated in the following
# example. The language can optionally be specified on the first line after the
# backticks, and is used for syntax highlighting.
#
#   ```c
#     x = y + z;
#     if ( zookoo == 2 )
#     {
#       foobar();
#     }
#   ```
#
# Note that the indentation of the first opening backticks and the last closing
# backticks must be exactly the same.  The code sequence itself should have a
# larger indentation than the surrounding braces.
#
re_code_start   = re.compile( r"(\s*)```([\w\+\#\-]+)?\s*$" )
re_code_end     = re.compile( r"(\s*)```\s*$" )

#
# A regular expression to isolate identifiers from other text.  Two syntax
# forms are supported:
#
#   <name>
#   <name>[<id>]
#
# where both `<name>' and `<id>' consist of alphanumeric characters, `_',
# and `-'.  Use `<id>' if there are multiple, valid `<name>' entries; in the
# index, `<id>' will be appended in parentheses.
#
# For example,
#
#   stem_darkening[autofit]
#
# becomes `stem_darkening (autofit)' in the index.
#
re_identifier = re.compile( r"""
                              ((?:\w|-)+
                               (?:\[(?:\w|-)+\])?)
                            """, re.VERBOSE )


#
# We collect macro names ending in `_H' (group 1), as defined in
# `freetype/config/ftheader.h'.  While outputting the object data, we use
# this info together with the object's file location (group 2) to emit the
# appropriate header file macro and its associated file name before the
# object itself.
#
# Example:
#
#   #define FT_FREETYPE_H <freetype.h>
#
re_header_macro = re.compile( r'^#define\s{1,}(\w{1,}_H)\s{1,}<(.*)>' )


################################################################
##
##  DOC CODE CLASS
##
##  The `DocCode' class is used to store source code lines.
##
##  `self.lines' contains a set of source code lines that will be dumped as
##  HTML in a <PRE> tag.
##
##  The object is filled line by line by the parser; it strips the leading
##  `margin' space from each input line before storing it in `self.lines'.
##
class  DocCode( object ):

    def  __init__( self, margin, lines, lang = None ):
        self.lines = []
        self.words = None
        self.lang = lang

        # remove margin spaces
        for l in lines:
            if l[:margin].strip(  ) == "":
                l = l[margin:]
            self.lines.append( l )

    def  dump( self, prefix = "" ):
        lines = self.dump_lines( 0 )
        for l in lines:
            print( prefix + l )

    def  dump_lines( self, margin = 0 ):
        result = []
        for l in self.lines:
            result.append( " " * margin + l )
        return result



################################################################
##
##  DOC PARA CLASS
##
##  `Normal' text paragraphs are stored in the `DocPara' class.
##
##  `self.words' contains the list of words that make up the paragraph.
##
class  DocPara( object ):

    def  __init__( self, lines, margin = -1 ):
        self.lines  = None
        self.words  = []
        self.indent = len( lines[0] ) - len( lines[0].lstrip() )
        first_line  = lines[0].strip()
        indent_diff = self.indent - margin

        if margin > 0 and indent_diff >= 4:
            # if the first line has an indentation >= 4,
            # add those spaces to it.
            indent_list = [''] * indent_diff
            self.words.extend( indent_list )
            # This para is indented, the next may also be relative
            # to the parent, so set indent to margin
            self.indent = margin

        self.words.extend( first_line.split() )

        for l in lines[1:]:
            l = l.strip()
            self.words.extend( l.split() )

    def  dump( self, prefix = "" ):
        lines = self.dump_lines( 0 )
        for l in lines:
            print( prefix + l )

    def  dump_lines( self, margin = 0, width = 60 ):
        cur    = ""  # current line
        col    = 0   # current width
        result = []

        for word in self.words:
            ln = len( word )
            if col > 0:
                ln = ln + 1

            if col + ln > width:
                result.append( " " * margin + cur )
                cur = word
                col = len( word )
            else:
                if col > 0:
                    cur = cur + " "
                cur = cur + word
                col = col + ln

        if col > 0:
            result.append( " " * margin + cur )

        return result


################################################################
##
##  DOC FIELD CLASS
##
##  The `DocField' class stores a list containing either `DocPara' or
##  `DocCode' objects.  Each DocField object also has an optional `name'
##  that is used when the object corresponds to a field or value definition.
##
class  DocField( object ):

    def  __init__( self, name, lines ):
        self.name  = name  # can be `None' for normal paragraphs/sources
        self.items = []    # list of items

        mode_none  = 0     # start parsing mode
        mode_code  = 1     # parsing code sequences

        margin     = -1    # current code sequence indentation
        cur_lines  = []
        indent     = -1
        lang       = None

        # analyze the markup lines to check whether they contain paragraphs,
        # code sequences, or fields definitions
        #
        mode  = mode_none

        for l in lines:
            # are we parsing a code sequence?
            if mode == mode_code:
                m = re_code_end.match( l )
                if m and len( m.group( 1 ) ) <= margin:
                    # that's it, we finished the code sequence
                    code = DocCode( 0, cur_lines, lang )
                    self.items.append( code )
                    margin    = -1
                    cur_lines = []
                    mode      = mode_none
                else:
                    # otherwise continue the code sequence
                    cur_lines.append( l[margin:] )
            else:
                # start of code sequence?
                m = re_code_start.match( l )
                if m:
                    # save current lines
                    if cur_lines:
                        para = DocPara( cur_lines )
                        self.items.append( para )
                        cur_lines = []

                    # switch to code extraction mode
                    margin = len( m.group( 1 ) )
                    lang   = m.group( 2 )
                    mode   = mode_code
                else:
                    if not l.split() and cur_lines:
                        # if the line is empty, we end the current paragraph,
                        # if any
                        para = DocPara( cur_lines, indent )
                        self.items.append( para )
                        # store indent value of current para
                        indent = para.indent
                        cur_lines = []
                    else:
                        # otherwise, simply add the line to the current
                        # paragraph
                        cur_lines.append( l )

        if mode == mode_code:
            # unexpected end of code sequence
            code = DocCode( margin, cur_lines, lang )
            self.items.append( code )
        elif cur_lines:
            para = DocPara( cur_lines, indent )
            self.items.append( para )

    def  dump( self, prefix = "" ):
        first = 1
        for p in self.items:
            if not first:
                print( "" )
            p.dump( prefix )
            first = 0

    def  dump_lines( self, margin = 0, width = 60 ):
        result = []
        nl     = None

        for p in self.items:
            if nl:
                result.append( "" )

            result.extend( p.dump_lines( margin, width ) )
            nl = 1

        return result


#
# A regular expression to detect field definitions.
#
# Examples:
#
#   foo     ::
#   foo.bar ::
#
re_field = re.compile( r"""
                         \s*
                           (
                             \w*
                           |
                             \w (\w | \.)* \w
                           )
                         \s* ::
                       """, re.VERBOSE )


################################################################
##
##  DOC MARKUP CLASS
##
class  DocMarkup( object ):

    def  __init__( self, tag, lines ):
        self.tag    = tag.lower()
        self.fields = []

        cur_lines = []
        field     = None

        for l in lines:
            m = re_field.match( l )
            if m:
                # We detected the start of a new field definition.

                # first, save the current one
                if cur_lines:
                    f = DocField( field, cur_lines )
                    self.fields.append( f )
                    cur_lines = []
                    field     = None

                field     = m.group( 1 )   # record field name
                ln        = len( m.group( 0 ) )
                l         = " " * ln + l[ln:]
                cur_lines = [l]
            else:
                cur_lines.append( l )

        if field or cur_lines:
            f = DocField( field, cur_lines )
            self.fields.append( f )

    def  get_name( self ):
        try:
            return self.fields[0].items[0].words[0]
        except Exception:
            return None

    def  dump( self, margin ):
        print( " " * margin + "<" + self.tag + ">" )
        for f in self.fields:
            f.dump( "  " )
        print( " " * margin + "</" + self.tag + ">" )


################################################################
##
##  DOC CHAPTER CLASS
##
class  DocChapter( object ):

    def  __init__( self, block ):
        self.block    = block
        self.sections = []
        if block:
            self.name  = block.name
            self.title = block.get_markup_words( "title" )
            self.order = block.get_markup_words( "sections" )
        else:
            self.name  = "Other"
            self.title = "Miscellaneous".split()
            self.order = []


################################################################
##
##  DOC SECTION CLASS
##
class  DocSection( object ):

    def  __init__( self, name = "Other" ):
        self.name        = name
        self.blocks      = {}
        self.block_names = []  # ordered block names in section
        self.defs        = []
        self.abstract    = ""
        self.description = ""
        self.order       = []
        self.title       = "ERROR"
        self.chapter     = None

    def  add_def( self, block ):
        self.defs.append( block )

    def  add_block( self, block ):
        self.block_names.append( block.name )
        self.blocks[block.name] = block

    def  process( self ):
        # look up one block that contains a valid section description
        for block in self.defs:
            title = block.get_markup_text( "title" )
            if title:
                self.title       = title
                self.abstract    = block.get_markup_words( "abstract" )
                self.description = block.get_markup_items( "description" )
                self.order       = block.get_markup_words_all( "order" )
                return

    def  reorder( self ):
        self.block_names = utils.sort_order_list( self.block_names,
                                                  self.order )


################################################################
##
##  CONTENT PROCESSOR CLASS
##
class  ContentProcessor( object ):

    def  __init__( self ):
        """Initialize a block content processor."""
        self.reset()

        self.sections = {}    # dictionary of documentation sections
        self.section  = None  # current documentation section

        self.chapters = []    # list of chapters

        self.headers  = {}    # dictionary of header macros

    def  set_section( self, section_name ):
        """Set current section during parsing."""
        if section_name not in self.sections:
            section = DocSection( section_name )
            self.sections[section_name] = section
            self.section                = section
        else:
            self.section = self.sections[section_name]

    def  add_chapter( self, block ):
        chapter = DocChapter( block )
        self.chapters.append( chapter )

    def  reset( self ):
        """Reset the content processor for a new block."""
        self.markups      = []
        self.markup       = None
        self.markup_lines = []

    def  add_markup( self ):
        """Add a new markup section."""
        if self.markup and self.markup_lines:

            # get rid of last line of markup if it's empty
            marks = self.markup_lines
            if len( marks ) > 0 and not marks[-1].strip():
                self.markup_lines = marks[:-1]

            m = DocMarkup( self.markup, self.markup_lines )

            self.markups.append( m )

            self.markup       = None
            self.markup_lines = []

    def  process_content( self, content ):
        """Process a block content and return a list of DocMarkup objects
        corresponding to it."""
        first        = 1

        margin  = -1
        in_code = 0

        for line in content:
            if in_code:
                m = re_code_end.match( line )
                if m and len( m.group( 1 ) ) <= margin:
                    in_code = 0
                    margin  = -1
            else:
                m = re_code_start.match( line )
                if m:
                    in_code = 1
                    margin  = len( m.group( 1 ) )

            found = None

            if not in_code:
                for t in sources.re_markup_tags:
                    m = t.match( line )
                    if m:
                        found  = m.group( 1 ).lower()
                        prefix = len( m.group( 0 ) )
                        # remove markup from line
                        line   = " " * prefix + line[prefix:]
                        break

            # is it the start of a new markup section ?
            if found:
                first = 0
                self.add_markup()  # add current markup content
                self.markup = found
                if len( line.strip() ) > 0:
                    self.markup_lines.append( line )
            elif first == 0:
                self.markup_lines.append( line )

        self.add_markup()

        return self.markups

    def  parse_sources( self, source_processor ):
        blocks = source_processor.blocks
        count  = len( blocks )

        for n in range( count ):
            source = blocks[n]
            if source.content:
                # this is a documentation comment, we need to catch
                # all following normal blocks in the "follow" list
                #
                follow = []
                m = n + 1
                while m < count and not blocks[m].content:
                    follow.append( blocks[m] )
                    m = m + 1

                DocBlock( source, follow, self )

    def  finish( self ):
        # process all sections to extract their abstract, description
        # and ordered list of items
        #
        for sec in self.sections.values():
            sec.process()

        # process chapters to check that all sections are correctly
        # listed there
        for chap in self.chapters:
            for sec in chap.order:
                if sec in self.sections:
                    section = self.sections[sec]
                    section.chapter = chap
                    section.reorder()
                    chap.sections.append( section )
                else:
                    log.warn( "Chapter '%s' in %s"
                        " lists unknown section '%s'",
                        chap.name, chap.block.location(), sec )

        # check that all sections are in a chapter
        #
        others = []
        for sec in self.sections.values():
            if not sec.chapter:
                sec.reorder()
                others.append( sec )

        # create a new special chapter for all remaining sections
        # when necessary
        #
        if others:
            chap = DocChapter( None )
            # Assign the chapter to all sections
            for section in others:
                section.chapter = chap
            chap.sections = others
            self.chapters.append( chap )


################################################################
##
##  DOC BLOCK CLASS
##
class  DocBlock( object ):

    def  __init__( self, source, follow, processor ):
        processor.reset()

        self.source  = source
        self.code    = []
        self.type    = "ERRTYPE"
        self.name    = "ERRNAME"
        self.section = processor.section
        self.markups = processor.process_content( source.content )

        # compute block type from first markup tag
        try:
            self.type = self.markups[0].tag
        except Exception:
            pass

        # compute block name from first markup paragraph
        try:
            markup = self.markups[0]
            para   = markup.fields[0].items[0]
            name   = para.words[0]
            m = re_identifier.match( name )
            if m:
                name = m.group( 1 )
            self.name = name
        except Exception:
            pass

        if self.type == "section":
            # detect new section starts
            processor.set_section( self.name )
            processor.section.add_def( self )
        elif self.type == "chapter":
            # detect new chapter
            processor.add_chapter( self )
        else:
            processor.section.add_block( self )

        # now, compute the source lines relevant to this documentation
        # block. We keep normal comments in for obvious reasons (??)
        source = []
        for b in follow:
            if b.format:
                break
            for l in b.lines:
                # collect header macro definitions
                m = re_header_macro.match( l )
                if m:
                    processor.headers[m.group( 2 )] = m.group( 1 )

                # we use "/* */" as a separator
                if sources.re_source_sep.match( l ):
                    break
                source.append( l )

        # now strip the leading and trailing empty lines from the sources
        start = 0
        end   = len( source ) - 1

        while start < end and not source[start].strip():
            start = start + 1

        while start < end and not source[end].strip():
            end = end - 1

        if start == end and not source[start].strip():
            self.code = []
        else:
            self.code = source[start:end + 1]

    def  location( self ):
        return self.source.location()

    def  get_markup( self, tag_name ):
        """Return the DocMarkup corresponding to a given tag in a block."""
        for m in self.markups:
            if m.tag == tag_name.lower():
                return m
        return None

    def  get_markup_words( self, tag_name ):
        try:
            m = self.get_markup( tag_name )
            return m.fields[0].items[0].words
        except Exception:
            return []

    def  get_markup_words_all( self, tag_name ):
        try:
            m = self.get_markup( tag_name )
            words = []
            for item in m.fields[0].items:
                # We honour empty lines in an `<Order>' section element by
                # adding the sentinel `/empty/'.  The formatter should then
                # convert it to an appropriate representation in the
                # `section_enter' function.
                words += item.words
                words.append( "/empty/" )
            return words
        except Exception:
            return []

    def  get_markup_text( self, tag_name ):
        result = self.get_markup_words( tag_name )
        return " ".join( result )

    def  get_markup_items( self, tag_name ):
        try:
            m = self.get_markup( tag_name )
            return m.fields[0].items
        except Exception:
            return None

# eof
