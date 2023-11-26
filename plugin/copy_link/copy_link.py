from talon import Context, Module, actions, clip

mod = Module()
ctx = Context()


@mod.action_class
class Actions:
    def copy_link(url: str, title: str):
        """Copy link to clipboard as RTF"""
        rtf = (
            rb'{\rtf1\ansi\ansicpg1252\uc1{\field{\*\fldinst {HYPERLINK "'
            + url.encode("rtfunicode")
            + rb'"}}{\fldrslt '
            + title.encode("rtfunicode")
            + rb"}}}"
        )
        mime = clip.MimeData()
        mime.urls = [url]
        mime.rtf = rtf.decode("ascii")
        # XXX can't set text or it *adds* an item
        clip.set_mime(mime)


# Below copied from https://github.com/mjpieters/rtfunicode

# Copyright (c) 2011, Martijn Pieters
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

#     Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#     Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Encode unicode strings to RTF 1.5-compatible command codes.
# Command codes are of the form `\uN?`, where N is a signed 16-bit integer and
# ? is a placeholder character for pre-1.5 RTF readers.

import codecs
import re
from struct import unpack

# Encode everything < 0x20, the \, { and } chars and everything > 0x7f.
# Codeponts over \uffff are handled separately so capture these in a second
# group. Valid surrogate pairs are supported too.
_charescape = re.compile(
    "([\x00-\x1f\\\\{}\x80-\ud7ff\ue000-\uffff])|"
    "([\U00010000-\U0001ffff]|[\ud800-\udbff][\udc00-\udfff])"
)


def _replace(match):
    # Convert codepoint into a signed integer
    char = match.group(1)
    if not char:
        # Encoding to UTF-16 is the simplest path to supporting surrogates.
        encoded = match.group(2).encode("utf-16-le")
        cp1, cp2 = unpack("<hh", encoded)
        # Microsoft RTF 1.9.1 specification (Word 2007), page 115, all
        # surrogates must be wrapped in a {/mr...} math text-run group.
        # Experimentation with various RTF apps (Word, Apple TextEdit,
        # LibreOffice) shows surrogates work in regular paragraphs too.
        return f"\\u{cp1}?\\u{cp2}?"
    cp = ord(char)
    return f"\\u{cp > 32767 and cp - 65536 or cp}?"


def _rtfunicode_encode(text, errors):
    # Encode to RTF \uDDDDD? signed 16 integers and replacement char
    return _charescape.sub(_replace, text).encode("ascii", errors)


class Codec(codecs.Codec):
    def encode(self, input, errors="strict"):
        return _rtfunicode_encode(input, errors), len(input)


class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return _rtfunicode_encode(input, self.errors)


class StreamWriter(Codec, codecs.StreamWriter):
    pass


def rtfunicode(name):
    if name == "rtfunicode":
        return codecs.CodecInfo(
            name="rtfunicode",
            encode=Codec().encode,
            decode=Codec().decode,
            incrementalencoder=IncrementalEncoder,
            streamwriter=StreamWriter,
        )


codecs.register(rtfunicode)
