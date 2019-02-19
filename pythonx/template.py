import vim
import re


class TextGenerator(object):
    def __init__(self):
        self.tpl = ""
        self.bufname = "[Render Result]"
        self.outwin = None
        self.outbuf = None

    def set_template(self, fl: int, ll: int):
        self.tpl = "\n".join(vim.current.buffer[fl:ll])

        # replace "{" to "{{", "}" to "}}" for rules of string.format
        self.tpl = re.sub(r'(?<!\d)}', '}}', self.tpl)
        self.tpl = re.sub(r'{(?!\d)', '{{', self.tpl)

    def unset_template(self):
        self.tpl = ""

    def render(self, fl, ll):
        winnr = vim.eval("win_getid()")
        b = vim.current.buffer
        data = b[fl:ll]

        if not self.tpl:
            self.tpl = b[fl - 1]

        if not self.outwin and not self.outbuf:
            vim.command("new")
            self.outbuf = vim.current.buffer
            self.outbuf.name = self.bufname
            # setlocal buftype=nofile
            self.outbuf.options["buftype"] = "nofile"
            # setlocal nobuflisted
            self.outbuf.options["buflisted"] = False
            # setlocal noswapfile
            self.outbuf.options["swapfile"] = False

            # setlocal bufhidden=hide
            # setlocal textwidth=0
            # setlocal nolist
            # setlocal nowrap
            # setlocal winfixwidth
            # setlocal nospell

            self.outwin = vim.current.window
            self.outwin.options["previewwindow"] = True

        if not self.outwin.valid:
            vim.command("sb %d" % self.outbuf.number)
            self.outwin = vim.current.window
            self.outwin.options["previewwindow"] = True
            # setlocal buftype=nofile
            self.outbuf.options["buftype"] = "nofile"

        vim.command("call win_gotoid(%s)" % winnr)
        # setlocal nomodifiable
        self.outwin.buffer.options["modifiable"] = True

        # clear outbuf
        del self.outwin.buffer[:]

        for d in data:
            self.outwin.buffer.append(
                    (self.tpl.format(*tuple(d.split()))).splitlines(),
                    0)
        self.outwin.buffer.options["modifiable"] = False
