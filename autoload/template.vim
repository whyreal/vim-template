exec "pythonx import template"
exec "pythonx tg = template.TextGenerator()"

function! template#RenderTemplate(fl, ll)
    exec "pythonx tg.render(int(" . a:fl . ") - 1, int(" . a:ll . "))"
endfunction

function! template#SetTemplate(fl, ll)
    exec "pythonx tg.set_template(int(" . a:fl . ") - 1, int(" . a:ll . "))"
endfunction

function! template#UnSetTemplate()
    exec "pythonx tg.unset_template()"
endfunction

