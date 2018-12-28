import vim
import re


class TextGenerator(object):
    def __init__(self):
        self.tpl = ""
        self.bufname = "[Result]"
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

        if not self.outbuf:
            vim.command("new")
            self.outbuf = vim.current.buffer
            self.outbuf.name = self.bufname

            # setlocal buftype=nofile
            self.outbuf.options["buftype"] = "nofile"
            # setlocal nobuflisted
            self.outbuf.options["buflisted"] = False

            # setlocal bufhidden=hide
            # setlocal noswapfile
            # setlocal textwidth=0

            # setlocal nolist
            # setlocal nowrap
            # setlocal winfixwidth
            # setlocal nospell
            vim.current.window.options["previewwindow"] = True
            vim.command("call win_gotoid(%s)" % winnr)

        # setlocal nomodifiable
        self.outbuf.options["modifiable"] = True

        # clear outbuf
        del self.outbuf[:]

        for d in data:
            self.outbuf.append(
                    (self.tpl.format(*tuple(d.split()))).splitlines(),
                    0)
        self.outbuf.options["modifiable"] = False
